from altitude import AltitudeInterpolator


al = AltitudeInterpolator()

img = al.elevation_image

max_brightness = 0
max_b_coords = []
last_p = 0
for x in range(al.x_dim):
    for y in range(al.y_dim):
        if sum(img.getpixel((x, y))) / 3 / 255 > max_brightness:
            max_brightness = sum(img.getpixel((x, y))) / 3 / 255
            max_b_coords = [x, y]
    if int((x / al.x_dim) * 100) > last_p:
        print("Progress: " + str(int((x / al.x_dim) * 100)) + "%")
        last_p = int((x / al.x_dim) * 100)

print("Max brightness:", max_brightness)
print("Max brightness coords:", max_b_coords)


# Max brightness: 1.0
# Max brightness coords: [6593, 7318]
# y_cord = lambda lat: np.digitize(al.y_dim - ((lat + 180) / 360 * al.y_dim), range(al.y_dim))
# x_cord = lambda lon: np.digitize((lon + 180) / 360 * al.x_dim, range(al.x_dim))
from PIL import ImageDraw2

draw = ImageDraw2(al.elevation_image)
draw.point(
    max_b_coords,
    fill=(255, 0, 0),
)
