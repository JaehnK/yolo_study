import json
import os
from PIL import Image

def convert_to_jpg(image_folder):
    normalized_paths = {}
    for filename in os.listdir(image_folder):
        name, ext = os.path.splitext(filename)
        if ext.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
            if ext.lower() != '.jpg':
                old_path = os.path.join(image_folder, filename)
                new_filename = f"{name}.jpg"
                new_path = os.path.join(image_folder, new_filename)
                try:
                    with Image.open(old_path) as img:
                        rgb_im = img.convert('RGB')
                        rgb_im.save(new_path, 'JPEG')
                    os.remove(old_path)  # 원본 파일 삭제
                    print(f"Converted and renamed: {filename} -> {new_filename}")
                    normalized_paths[name] = new_filename
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}. Skipping this file.")
                    normalized_paths[name] = filename
            else:
                if ext == '.JPG':
                    new_filename = f"{name}.jpg"
                    old_path = os.path.join(image_folder, filename)
                    new_path = os.path.join(image_folder, new_filename)
                    try:
                        os.rename(old_path, new_path)
                        print(f"Renamed: {filename} -> {new_filename}")
                        normalized_paths[name] = new_filename
                    except Exception as e:
                        print(f"Error renaming {filename}: {str(e)}. Skipping this file.")
                        normalized_paths[name] = filename
                else:
                    normalized_paths[name] = filename
    return normalized_paths

def get_image_size(image_path):
    with Image.open(image_path) as img:
        return img.size

def convert_to_yolo_format(json_data, image_folder):
    yolo_labels = []
    
    for image_name, data in json_data.items():
        image_path = os.path.join(image_folder, f"{image_name}.jpg")  # 확장자는 실제 이미지 형식에 맞게 조정하세요
        
        if not os.path.exists(image_path):
            print(f"Warning: Image file not found for {image_name}")
            continue
        
        image_width, image_height = get_image_size(image_path)
        crop_raw = data['crop_raw']
        
        # YOLO 형식으로 변환
        x_center = (crop_raw[0] + crop_raw[2] / 2) / image_width
        y_center = (crop_raw[1] + crop_raw[3] / 2) / image_height
        width = crop_raw[2] / image_width
        height = crop_raw[3] / image_height
        
        # 클래스 ID는 0으로 가정 (단일 클래스)
        yolo_label = f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
        yolo_labels.append((image_name, yolo_label))
    
    return yolo_labels

with open("./properties.json", 'r') as f:
    json_data = json.load(f)

image_folder = "./combined_food_dataset"
convert_to_jpg(image_folder)
yolo_labels = convert_to_yolo_format(json_data, image_folder)

# 결과를 파일에 저장
output_folder = "./label"
os.makedirs(output_folder, exist_ok=True)

for image_name, label in yolo_labels:
    with open(os.path.join(output_folder, f"{image_name}.txt"), "w") as f:
        f.write(label)

print("YOLO 형식의 레이블 파일이 생성되었습니다.")