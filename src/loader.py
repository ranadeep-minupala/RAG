import json

def load(policies_path, faq_path, get_business_info_path):
    with open(policies_path, "r",encoding="utf-8") as f:
        policies_text = f.read()
    with open(faq_path, "r",encoding="utf-8") as f:
        faq_text = f.read()
    with open(get_business_info_path, "r") as f:
        business_info = json.load(f)
    return policies_text, faq_text, business_info