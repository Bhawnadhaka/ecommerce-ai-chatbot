import pandas as pd
from langchain_core.documents import Document

def dataconveter():
    product_data = pd.read_csv(
        r"C:\Users\91935\OneDrive\Desktop\Projects\E-Commerce Chatbot\data\Product_review_dataset.csv",
        encoding='latin1'
    )

    data = product_data[["Product_name", "Review"]]

    product_list = []
    for index, row in data.iterrows():
        # Skip rows with missing review
        if pd.isna(row['Review']):
            continue
        obj = {
            'Product_name': row['Product_name'],
            'Review': row['Review']
        }
        product_list.append(obj)

    docs = []
    for entry in product_list:
        metadata = {"Product_name": entry['Product_name']}
        doc = Document(page_content=str(entry['Review']), metadata=metadata)
        docs.append(doc)
    return docs