from os.path import expanduser
from shutil import copytree
from argparse import ArgumentParser

parser = ArgumentParser(description='Prepare directory to be pushed to Heroku Server')
parser.add_argument('dest', help='path where the contents needs to be copied')

args = parser.parse_args()

dest = expanduser(args.dest)
app_dest_path =  dest + '/App'
config_path = 'Heroku_Setup/Config'
data_dest_path = dest + '/Data'
recommender_dest_path = dest + '/ML_Pipeline'

copytree('Flask_App', app_dest_path, dirs_exist_ok=True)
copytree('ML_Pipeline', recommender_dest_path, dirs_exist_ok=True)
copytree('Data', data_dest_path, dirs_exist_ok=True)

copytree(config_path, dest, dirs_exist_ok=True)
print('Done...')
print('Make sure to link a postgres database')