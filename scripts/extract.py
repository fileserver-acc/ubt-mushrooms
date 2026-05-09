import os
import fitz
from tqdm import tqdm
from extract_images import extract
import sys
from PIL import Image


def extract(source: str, destination: str):
    pdf_file = fitz.open(source)

    for page_index in tqdm(range(len(pdf_file))):
        page = pdf_file.load_page(page_index)
        image_list = page.get_images(full=True)

        for image_index, img in enumerate(image_list, start=1):
            xref = img[0]

            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]

            image_ext = base_image["ext"]

            image_name = f"image{page_index+1}_{image_index}.{image_ext}"
            with open(destination + "/" + image_name, "xb") as image_file:
                image_file.write(image_bytes)


if __name__ == "__main__":
    indir = sys.argv[1]
    outdir = sys.argv[2]

    for each_path in tqdm(os.listdir(indir)):
        if ".pdf" in each_path:
            print(f"extracting from {each_path}...")
            doc = fitz.Document((os.path.join(indir, each_path)))

            if not (os.path.exists(os.path.join(outdir, each_path.split("/").pop().split(".")[0])) and os.path.isdir(os.path.join(outdir, each_path.split("/").pop().split(".")[0]))):
                os.makedirs(os.path.join(outdir, each_path.split("/").pop().split(".")[0]), exist_ok=True)

            try:
                extract(os.path.join(indir, each_path), os.path.join(outdir, each_path.split("/").pop().split(".")[0]))
            except Exception as e:
                print(f"error extracting file {each_path}: {e}", file=sys.stderr)
