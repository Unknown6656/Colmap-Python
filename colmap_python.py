import os
import argparse
import subprocess


parser = argparse.ArgumentParser(description = "Process images using COLMAP.")
parser.add_argument('-i', '--image-dir', action = "store", dest = "image_dir", required = True, help = "The input image directory")
parser.add_argument('-p', '--project-dir', action = "store", dest = "project_dir", required = True, help = "The project directory")
parser.add_argument('-c', '--colmap', action = "store", dest = "colmap_binary", default = "colmap", help = "The path pointing to the COLMAP binary")
parser.add_argument('-o', '--output-name', action = "store", dest = "output_name", default = "render", help = "The name of the output file without the file extension (to be stored inside the project path)")
args = parser.parse_args()

current_dir = os.getcwd()
sparse_dir = f'{args.project_dir}/sparse'
dense_dir = f'{args.project_dir}/dense'
database_path = f'{args.project_dir}/database.db'

os.mkdir(dense_dir)
os.mkdir(sparse_dir)

stereo_type = "COLMAP"
max_img_size = 2000

output_name = "render"


# WORKFLOW COPIED FROM http://colmap.github.io/cli


# subprocess.run([args.colmap_binary, "automatic_reconstructor", "--workspace_path", args.project_dir, "--image_path", args.image_dir])
subprocess.run([args.colmap_binary, "feature_extractor", "--database_path", database_path, "--image_path", args.image_dir])
subprocess.run([args.colmap_binary, "exhaustive_matcher", "--database_path", database_path])
subprocess.run([args.colmap_binary, "mapper", "--database_path", database_path, "--output_path", sparse_dir, "--image_path", args.image_dir])
subprocess.run([args.colmap_binary, "image_undistorter", "--input_path", f'{sparse_dir}/0', "--output_path", dense_dir, "--image_path", args.image_dir, "--output_type", stereo_type, "--max_image_size", max_img_size])
subprocess.run([args.colmap_binary, "patch_match_stereo", "--workspace_path", dense_dir, "--workspace_format", stereo_type, "--PatchMatchStereo.geom_consistency", "true"])
subprocess.run([args.colmap_binary, "stereo_fusion", "--workspace_path", dense_dir, "--workspace_format", stereo_type, "--input_type", "geometric", "--output_path", f'{args.project_dir}/{args.output_name}.ply'])
subprocess.run([args.colmap_binary, "poisson_mesher", "--input_path", f'{args.project_dir}/{args.output_name}.ply', "--output_path", f'{args.project_dir}/{args.output_name}-poisson.ply'])
subprocess.run([args.colmap_binary, "delaunay_mesher", "--input_path", f'{args.project_dir}/{args.output_name}.ply', "--output_path", f'{args.project_dir}/{args.output_name}-delaunay.ply'])
