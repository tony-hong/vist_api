#!/usr/bin/env python
# coding: utf-8

# In[105]:


import math
import os
import os.path as osp
import json
from datetime import datetime
from pprint import pprint
from scipy.misc import imread, imresize
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams['figure.figsize'] = (10, 10)


# ### VIST directory

# In[106]:


annotations_dir = '/Users/tonyhong/ROOT/coli/SIND/data'
images_dir = ''


# In[196]:


split = 'test'
# Load dii's split json
b = datetime.now()
path_to_dii_val = osp.join(annotations_dir, 'dii', split+'.description-in-isolation.json')
dii = json.load(open(path_to_dii_val))
print 'dii\'s [%s] loaded. It took %.2f seconds.' % (split, (datetime.now() - b).total_seconds())

# Load sis's split json
b = datetime.now()
path_to_sis_val = osp.join(annotations_dir, 'sis', split+'.story-in-sequence.json')
sis = json.load(open(path_to_sis_val))
print 'sis\'s [%s] loaded. It took %.2f seconds.' % (split, (datetime.now() - b).total_seconds())


# In[199]:


split = 'train'
# Load dii's split json
b = datetime.now()
path_to_dii_val = osp.join(annotations_dir, 'dii', split+'.description-in-isolation.json')
dii_train = json.load(open(path_to_dii_val))
print 'dii\'s [%s] loaded. It took %.2f seconds.' % (split, (datetime.now() - b).total_seconds())

# Load sis's split json
b = datetime.now()
path_to_sis_val = osp.join(annotations_dir, 'sis', split+'.story-in-sequence.json')
sis_train = json.load(open(path_to_sis_val))
print 'sis\'s [%s] loaded. It took %.2f seconds.' % (split, (datetime.now() - b).total_seconds())


split = 'val'
# Load dii's split json
b = datetime.now()
path_to_dii_val = osp.join(annotations_dir, 'dii', split+'.description-in-isolation.json')
dii_val = json.load(open(path_to_dii_val))
print 'dii\'s [%s] loaded. It took %.2f seconds.' % (split, (datetime.now() - b).total_seconds())

# Load sis's split json
b = datetime.now()
path_to_sis_val = osp.join(annotations_dir, 'sis', split+'.story-in-sequence.json')
sis_val = json.load(open(path_to_sis_val))
print 'sis\'s [%s] loaded. It took %.2f seconds.' % (split, (datetime.now() - b).total_seconds())


# In[108]:


# Let's check one ann
sis.keys()


# In[109]:


sis['annotations'][0]


# In[110]:


sis['images'][0]


# In[111]:


sis['albums'][3]


# In[112]:


def show_album(alb_id):
    img_ids = alb_to_img_ids[alb_id]
    plt.figure()
    cols = 5
    rows = math.ceil(len(img_ids)/float(cols))
    for i, img_id in enumerate(img_ids):
        img = Images[img_id]
        img_file = osp.join(images_dir, split, img['id']+'.jpg')
#         img_content = imread(img_file)
#         img_content = imresize(img_content, (224, 224))
        ax = plt.subplot(rows, cols, i+1)
#         ax.imshow(img_content)
        ax.axis('off')
        ax.set_title(str(img_id)+'\n'+img['datetaken'][4:])
        print(img['url_o'])
    plt.show()


# In[338]:


def show_story(story_id, show_image=True):
    result = []
    sent_ids = story_to_sent_ids[story_id]
    if show_image:
        plt.figure()
        for i, sent_id in enumerate(sent_ids):
            img_id = Sents[sent_id]['img_id']
            img = Images[img_id]
            img_file = osp.join(images_dir, split, str(img_id)+'.jpg')
#             img_content = imread(img_file)
#             img_content = imresize(img_content, (224, 224))
            ax = plt.subplot(1, len(sent_ids), i+1)
#             ax.imshow(img_content)
            ax.axis('off')
            ax.set_title(str(img_id)+'\n'+img['datetaken'][5:])
            print(img['url_o'])
        plt.show()
    for sent_id in sent_ids:
        sent = Sents[sent_id]
        img_id = sent['img_id']
        img = Images[img_id]
        line = '[%s], text[%s], image_url:\n %s' % (sent['order'], sent['original_text'], img['url_o'])
        result.append(line)
        print line
    return result


# In[288]:


all_imgs = sis['images'] + sis_train['images'] + sis_val['images']
all_albums = sis['albums'] + sis_train['albums'] + sis_val['albums']

Images = {item['id']: item for item in sis_train['images']}
Albums = {item['id']: item for item in sis_train['albums']}
alb_to_img_ids = {}
for item in sis_train['images']:
    alb_id = item['album_id']
    img_id = item['id']
    alb_to_img_ids[alb_id] = alb_to_img_ids.get(alb_id, []) + [img_id]

# sort img_ids based on datetime
def getDateTime(img_id):
    x = Images[img_id]['datetaken']
    return datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
# for alb_id, img_ids in alb_to_img_ids.items():
#     img_ids.sort(key=getDateTime)


# In[289]:


# make sents = [{}]
sents = []
for ann in sis_train['annotations']:
    sent = ann[0].copy()
    sent['id'] = sent.pop('storylet_id')
    sent['order'] = sent.pop('worker_arranged_photo_order')
    sent['img_id'] = sent.pop('photo_flickr_id')
    sents += [sent]
Sents = {sent['id']: sent for sent in sents}

# story_id -> sent_ids
story_to_sent_ids = {}
for sent_id, sent in Sents.items():
    story_id = sent['story_id']
    story_to_sent_ids[story_id] = story_to_sent_ids.get(story_id, []) + [sent_id]

def get_order(sent_id):
    return Sents[sent_id]['order']
for story_id, sent_ids in story_to_sent_ids.items():
    sent_ids.sort(key=get_order)
    
# alb_id -> story_ids
alb_to_story_ids = {}
for story_id, sent_ids in story_to_sent_ids.items():
    sent = Sents[sent_ids[0]]
    alb_id = sent['album_id']
    alb_to_story_ids[alb_id] = alb_to_story_ids.get(alb_id, []) + [story_id]


# In[286]:


alb_id = '72157607155047588'
show_album(alb_id)


# In[ ]:


story_ids = alb_to_story_ids[alb_id]
print 'This album has %s stories.' % len(story_ids)
show_story(story_ids[4], True)


# In[ ]:


# alb_ids = Albums.keys()
# alb_id = alb_ids[2]; print alb_id
# show_album(alb_id)


# In[ ]:


sis['type']


# In[ ]:


dii.keys()


# In[121]:


pprint(dii['annotations'][0][0])
pprint(dii['annotations'][5][0])


# In[122]:


sis['annotations'][0][0]


# In[123]:


sis['albums'][0]['id']


# In[124]:


for i in range(len(sis['albums'])):
    if not sis['albums'][i]['id'] == dii['albums'][i]['id']:
        print 'inconsitancy found.'


# In[125]:


sis['albums'][0]


# In[126]:


sis['images'][7]['id']


# In[127]:


sis['annotations'][14]


# In[128]:


dii['annotations'][14]


# In[129]:


for i in range(len(sis['annotations'][:2])):
    sd = sis['annotations'][i][0]
    dd = dii['annotations'][i][0]
    if sd['album_id'] != dd['album_id'] or sd['photo_flickr_id'] != dd['photo_flickr_id']          or sd['worker_arranged_photo_order'] != dd['photo_order_in_story']:
            print 'k'


# In[163]:


import visual_genome.local as vg


# In[175]:


VG_img_dats = vg.get_all_image_data('/Users/tonyhong/ROOT/coli/VisualGenome')


# In[178]:


len(VG_img_dat)


# In[330]:


flickr2VG = dict()
for i, VG_img in enumerate(VG_img_dats):
    flickr2VG[str(VG_img.flickr_id)] = i
#     if VG_img.flickr_id:
#     print VG_img.flickr_id
len(VG_flickr_ids)


# In[246]:


VG_ids = set(flickr2VG.keys())
# flickr2VG[2835098587]


# In[ ]:





# In[248]:


len_sis_test = len(sis['images'])
SIND_test_ids = {img['id'] for img in sis['images']}
SIND_train_ids = {img['id'] for img in sis_train['images']}
SIND_val_ids = {img['id'] for img in sis_val['images']}
print len(SIND_train_ids)
print len(SIND_val_ids)


# In[ ]:





# In[250]:


flickr2VG.keys()[0]


# In[251]:


joint_set = set()
joint_set.update(VG_ids & SIND_train_ids)
joint_set.update(VG_ids & SIND_test_ids)
joint_set.update(VG_ids & SIND_val_ids)
joint_list = list(joint_set)
len(joint_list)


# In[253]:


flickr2VG['497007959']


# In[327]:


import re

# print len(Images)
story_dict = dict()
for idx in joint_list:
    if Images.get(idx, -1) != -1:
#         print('image_id', idx)
        album_id = Images[idx]['album_id']
#         print('album_id', album_id)
        story_ids = alb_to_story_ids[album_id]
#         print('story_ids', story_ids)
        for story_id in story_ids:
            sent_ids = story_to_sent_ids[story_id]
            for sent_id in sent_ids:
                sent_img_id = Sents[sent_id]['img_id']
                if sent_img_id == idx:
                    sent = Sents[sent_id]['text']
                    if re.search(r'time|photo', sent):
                        continue
                    story_dict[story_id] = idx
#         print '\n'
        
len(story_dict)


# In[328]:


of = open('output.txt', 'w')
for it in story_dict.items():
    print it[1]
    show_story(it[0], False)
    print ''
    print ''


# In[333]:


VG_img_dat[flickr2VG['21555842']]


# In[337]:


graph = api.get_scene_graph_of_image(id=2321518)
graph.relationships


# In[ ]:





# In[ ]:




