# import advertools as adv
# import pandas as pd

# adv.crawl('https://amazon.com', 'my_output_file.jl', follow_links=True)
# crawl_df = pd.read_json('my_output_file.jl', lines=True)

from bs4 import BeautifulSoup
import re


html = """
https://www.amazon.in/
"""

def processor(tag):
    href = tag.get('href')
    if not href: return False
    return True if (href.find("google") == -1) else False

soup = BeautifulSoup(html,features='html.parser')
back_links = soup.findAll(processor, href=re.compile(r"^https"))
print(back_links)
# import json
  
# # Data to be written
# dictionary ={
#     "name" : "sathiyajith",
#     "rollno" : 56,
#     "cgpa" : 8.6,
#     "phonenumber" : "9976770500"
# }
  
# Serializing json 
# json_object = json.dumps(dictionary, indent = 4)
  
# # Writing to sample.json
# with open("sample.json", "w") as outfile:
#     outfile.write(json_object)

# import json

# b = [
# 'Introduction',
# 'Wellard Testimonial',
# 'Where to Get Your Herbs',
# 'Principles: Why Herbs May Not Be Working For You',
# 'Principles: Look for the Cause',
# 'Principles: Preserving Herbs',
# 'Principles: Different Herbal Preparation Methods',
# 'Principles: Herbal Dosage',
# 'Principles: Herbs in Conjuction with Drug Medication Dosage',
# 'Principles: Herbal Resources',
# 'Principles: Herb Menstruum',
# 'Principles: Therapeutic Range',
# 'Principles: Herbs & Pregnancy',
# 'Principles: Different Forms of Herbal Medicine',
# 'Principles: The Difference Between Allopathic and Herbal Medicine',
# 'Herb Categories',
# 'Herbal Formulas: Elderberry Syrup',
# 'Herbal Formulas: Vitex Extract',
# 'Herbal Formulas: Sleep Formula',
# 'Herbal Formulas: Anti-Aging Tea',
# 'Herbal Formulas: Blook Suger Formula',
# 'Herbal Formulas: Energy Boost Formula',
# 'Herbal Formulas: Calming Infant Formula',
# 'Herbal Formulas: Herbal Nutritive Tonic',
# 'Herbal Formulas: Herbal Skin Cream',
# 'Herbal Formulas: Memory Enhancer',
# 'Herbal Formulas: Pain Salve',
# 'Herbal Formulas: Herbal Lip Balm',
# 'Herbal Formulas: Charcoal Poultice',
# 'Herbal Formulas: Herbal Relaxing Bath',
# 'Herbal Formulas: Comfrey Compress',
# 'Herbal Formulas: Herbal Skin Defoliator',
# 'Herbal Formulas: Skin Moisturizer',
# 'Herbal Formulas: Herbal Steam Inhalation',
# 'Herbal Formulas: Herbal Tea for Allergies',
# 'Herbal Formulas: Herbal Toothpaste',
# 'Herbal Formulas: Menopause Support',
# 'Herbs: Garlic',
# 'Herbs: Aloe Vera',
# 'Herbs: Elderberry',
# 'Herbs: Licorice',
# 'Herbs: Red Clover',
# 'Herbs: Ginkgo Biloba',
# 'Herbs: Vitex',
# 'Herbs: Cayenne Pepper',
# 'Herbs: Echinacea',
# 'Herbs: Ginseng',
# 'Herbs: Lavender',
# 'Herbs: Thyme',
# 'Herbs: Oregano',
# 'Herbs: St. Johns Wort',
# 'Herbs: Calendula',
# 'Herbs: Comfrey',
# 'Herbs: Plantain',
# 'Herbs: Turmeric',
# 'Herbs: Ginger'
# ]

# v = 1
# for r in b:
#     a = {
#         "title": r,
#         "description": "string",
#         "course_uuid": "fdd839c5-9c28-4366-bab7-d067e4dcabb0",
#         "author": "string",
#         "tags": "string",
#         "lesson_number": v,
#         "created_by": "6817e54b-d7e5-44cc-86d4-a6cc7c12be3a",
#         "updated_by": "6817e54b-d7e5-44cc-86d4-a6cc7c12be3a"
#         }
    
#     v +=1
#     print(json.dumps(a, indent=1))

