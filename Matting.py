# import pygame as pygame
# from matting import alpha_matting, save_image, stack_images, \
#     estimate_foreground_background, METHODS, PRECONDITIONERS
# import os
# import ImageLoader as imageLoader
#
# # Input paths
# image_path = "//home/kow/PycharmProjects/ImageBkRemoval/Images/bike.jpg"
# trimap_path = "/home/kow/PycharmProjects/ImageBkRemoval/Images/bike_mask.jpg"
# new_background_path = "/home/kow/PycharmProjects/ImageBkRemoval/Images/Background.jpg"
#
# # Output paths
# alpha_path = "out/person_alpha_%s_%s.png"
# cutout_path = "out/person_cutout_%s_%s.png"
# os.makedirs("out", exist_ok=True)
#
# img = pygame.image.load(image_path)
# height = img.get_height()
# width = img.get_width()
# image = imageLoader.load_image(image_path, "RGB", "BILINEAR", height=height)
#
# img = pygame.image.load(trimap_path)
# height = img.get_height()
# width = img.get_width()
# trimap = imageLoader.load_image(trimap_path, "GRAY", "NEAREST", height=height)
#
# for method in METHODS:
#     for preconditioner in PRECONDITIONERS[method]:
#
#         try:
#             alpha = alpha_matting(
#                 image, trimap,
#                 method, preconditioner,
#                 print_info=True)
#
#             # Save alpha
#             save_image(alpha_path % (method, preconditioner), alpha)
#
#             foreground, background = estimate_foreground_background(
#                 image, alpha, print_info=True)
#
#             # Make new image from foreground and alpha
#             cutout = stack_images(foreground, alpha)
#
#             # Save cutout
#             save_image(cutout_path % (method, preconditioner), cutout)
#         except:
#             continue
