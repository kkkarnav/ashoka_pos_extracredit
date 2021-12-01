from PIL import Image
import numpy as np


def compare_colours(base_colour, test_colour):

    for rgb_index, value in enumerate(base_colour):
        if not value + 10 >= test_colour[rgb_index] >= value - 10:
            return False
    return True


# get the temperatures and mean temperature for a given month
def find_temperatures(image, temperature_colours):

    month_temperatures = []

    # for row in range(184, 185, 20):  # for equator only
    for row in range(30, 340, 20):  # for every latitude
        for column in range(60, 780, 20):

            pixel_colour = image[row][column]
            # print(f"image[{row}][{column}]")

            for temperature, colour in temperature_colours:
                if compare_colours(pixel_colour, colour):
                    month_temperatures.append(temperature)
                    break

    mean_temp = sum(month_temperatures) / len(month_temperatures)

    return month_temperatures, mean_temp


def main():
    temperature_colours = [
        (-55, [5, 36, 79, 255]),
        (-50, [6, 56, 110, 255]),
        (-45, [8, 78, 150, 255]),
        (-40, [33, 109, 174, 255]),
        (-35, [59, 139, 194, 255]),
        (-30, [82, 160, 205, 255]),
        (-25, [102, 177, 212, 255]),
        (-20, [127, 194, 218, 255]),
        (-15, [156, 212, 225, 255]),
        (-10, [184, 228, 238, 255]),
        (-5, [199, 231, 241, 255]),
        (0, [255, 255, 180, 255]),
        (5, [255, 241, 143, 255]),
        (10, [253, 224, 107, 255]),
        (15, [248, 208, 84, 255]),
        (20, [241, 184, 60, 255]),
        (25, [236, 150, 38, 255]),
        (30, [229, 116, 18, 255]),
        (35, [209, 94, 10, 255]),
        (40, [199, 69, 1, 255]),
        (45, [161, 63, 11, 255]),
        (50, [132, 40, 21, 255]),
    ]

    year_temps = []

    for month in range(1, 13):

        # open the image
        image = np.asarray(
            Image.open(
                f"./pos_images/00cntl_temp_surface_{month if len(str(month)) >= 2 else ('0' + str(month))}_pm.png"
            ).convert("RGBA")
        )

        # get the mean temperature for this month
        month_temps, mean_temp = find_temperatures(image, temperature_colours)
        print(
            f"mean temperature for month {month}: {str(mean_temp)[:5]} degrees celsius"
        )
        year_temps.append(mean_temp)

    # get the annual mean
    print(sum(year_temps)/len(year_temps))


if __name__ == "__main__":
    main()
