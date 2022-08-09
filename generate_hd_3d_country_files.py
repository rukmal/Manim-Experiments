from country_data import CountryData
import trimesh as tri
import time

country = "LKA"
resolutions = [int(10**i) for i in range(2, 5)]

# times = []
# for resolution in resolutions:
#     print("Currently on resolution: {}".format(resolution))
#     tic = time.time()
#     # Get country trimesh in desired resolution
#     _, _, tm = CountryData().get_country_verts_and_tris(
#         country, resolution=resolution, return_trimesh=True
#     )
#     toc = time.time() - tic
#     times.append([resolution, toc])

tic = time.time()

# Get country trimesh in desired resolution
_, _, tm = CountryData().get_country_verts_and_tris(
    country, resolution=int(1e6), return_trimesh=True
)

# Save mesh as dae file
with open("mesh.dae", "wb") as f:
    f.write(tri.exchange.dae.export_collada(tm))


print(
    "TOOK {} SECONDS!!, {} MINUTES!!! {} HOURS!!!!!!!".format(
        time.time() - tic, (time.time() - tic) / 60, (time.time() - tic) / 3600
    )
)
