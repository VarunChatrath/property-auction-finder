import requests

DOCUMENT_URL = (
    "https://ibapi.in/Sale_Info_Home.aspx/getCarouselData"
)


def get_property_documents(property_id):

    payload = {
        "prop_id": property_id
    }

    response = requests.post(
        DOCUMENT_URL,
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    raw_data = response.json()["d"]

    files = raw_data.split("^^^^^")

    photo_url = None
    pdf_url = None

    for file_path in files:

        if ".jpg" in file_path.lower():

            filename = file_path.split("\\")[-1]

            photo_url = (
                f"https://ibapi.in/upload_saleinfo/"
                f"{property_id}/{filename}"
            )

        if ".pdf" in file_path.lower():

            filename = file_path.split("\\")[-1]

            pdf_url = (
                f"https://ibapi.in/upload_saleinfo/"
                f"{property_id}/{filename}"
            )

    return {
        "photo_url": photo_url,
        "pdf_url": pdf_url
    }


if __name__ == "__main__":

    result = get_property_documents(
        "BARB104220200001"
    )

    print(result)