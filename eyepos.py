import sys, math
import matplotlib.image as mpimg

_max_count = 25
_arm_len = 3

def main():
    imgpath = sys.argv[1]
    img = mpimg.imread(imgpath)
    height = len(img)
    width = len(img[0])

    row = [grayscale(x) for x in img[height / 2]]
    thresh = (min(row) + max(row)) / 2
    apply_thresh = lambda x: 1 if x >= thresh else 0
    start = [-1,-1]
    for i in range(width / 2):
        if start[0] == -1 and apply_thresh(row[width / 2 + i]) == 1:
            start[0] = width / 2 + i - 1
        if start[1] == -1 and apply_thresh(row[width / 2 - i]) == 1:
            start[1] = width / 2 - i + 1

        if start[0] != -1 and start[1] != -1:
            break

    p1 = p2 = [start[0], height / 2]
    p3 = p4 = [start[1], height / 2]
    count = 0
    while count < _max_count:
        skip_p2 = skip_p4 = False
        for i in range(8):
            angle = i * math.pi / 4
            if not skip_p2:
                x2 = int(math.ceil(_arm_len * math.cos(angle) + p2[0]))
                y2 = int(math.ceil(_arm_len * math.sin(angle) + p2[1]))
                if apply_thresh(grayscale(img[y2][x2])) == 0:
                    p2 = [x2, y2]
                    skip_p2 = True

            if not skip_p4:
                x4 = int(math.ceil(_arm_len * math.cos(angle) + p4[0]))
                y4 = int(math.ceil(_arm_len * math.sin(angle) + p4[1]))
                if apply_thresh(grayscale(img[y4][x4])) == 0:
                    p4 = [x4, y4]
                    skip_p4 = True

            if skip_p2 and skip_p4:
                break
        count += _arm_len

    c1 = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
    c2 = [(p3[0] + p4[0]) / 2, (p3[1] + p4[1]) / 2]
    m1 = -1 / slope(p1, p2)
    m2 = -1 / slope(p3, p4)
    x = ((-m1 * c1[0] + c1[1] - c2[1]) / m2 + c2[0]) / (1 - m1 / m2)
    y = m1 * (x - c1[0]) + c1[1]
    print [x, y]

def grayscale(x):
    return sum(x) / 3

def slope(p1, p2):
    return (p2[1] - p1[1]) / (p2[0] - p1[0])

main()