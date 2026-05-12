from ultralytics import YOLO
import os
from tqdm import tqdm
import sys

model_path = sys.argv[1]
pages_folder = sys.argv[2]
out_folder = sys.argv[3]

try:
    model = YOLO(model_path)

    os.makedirs(os.path.join(out_folder, "boxes"), exist_ok=True)

    page_paths = []
    batch = []
    paths = os.listdir(pages_folder)

    paths.sort(key=lambda a: int(a.split("_")[0].removeprefix("image")))
    for each_path in paths:
        print(each_path)
        batch.append(os.path.join(pages_folder, each_path))
        if len(batch) >= 50:
            page_paths.append(batch)
            batch = []
    
    page_paths.append(batch)


    for s in tqdm(range(len(page_paths))):
        print("starting batch " + str(s + 1))
        # Run batched inference on a list of images
        results = model(page_paths[s])  # return a list of Results objects

        # Process results list
        for (i, result) in enumerate(results):
            with open(os.path.join(out_folder, "boxes/" + result.path + ".box"), "w") as file:
                res = str(result.orig_shape)
                for b in result.boxes.xyxy:
                    res += "\n" + str(b.tolist())
                file.write(res)
                

            if len(result.boxes) != 0:
                result.save_crop(save_dir=out_folder)  # save to disk

        print("saved!\n")
except Exception as e:
    print(f"error segmenting image: {e}")
