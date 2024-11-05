
from skimage.metrics import structural_similarity as ssim
import cv2


class Similarity_Model:

    def __init__(self):
        pass


    def compare(self, path_img1, path_img2):

        print(f"{path_img1}  ||  {path_img2}")

        img1 = cv2.imread(path_img1)
        img2 = cv2.imread(path_img2)

        img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

        gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray_img2 = cv2.cvtColor(img2_resized, cv2.COLOR_BGR2GRAY)

        similarity, _ = ssim(gray_img1, gray_img2, full=True)

        return similarity if similarity > 0 else 0