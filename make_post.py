import json
from hashlib import sha256
from time import time
import argparse
import coloredlogs
import logging

coloredlogs.install(level='DEBUG')

parser = argparse.ArgumentParser(description='''Make posts to be stored on the Drone Gallery backend''')

parser.add_argument('-f', '--file', help='File to make/edit', required=True)

args = parser.parse_args()

def save(contents):
	with open(args.file, 'w', encoding='utf-8') as f:
		f.write(json.dumps(contents))
	logging.info(f"Saved {len(contents['posts'])} posts")

try:
	with open(args.file, 'r', encoding='utf-8') as f:
		contents = json.loads(f.read())
except FileNotFoundError:
	logging.info(f"Making new file {args.file}")
	contents = json.loads("""
		{
		"posts": []
		}
		""")
finally:
	logging.info(f"Loaded {len(contents['posts'])} posts")

while True:
	logging.info('Make Post [p] Delete Post [d] Read posts [r] Save [s] Save & Exit [x]')
	command = input(": ").lower()
	if command == 'x': # Exit
		# Finished
		save(contents)
		break
	elif command == 's': # Save
		save(contents)

	elif command == 'p': # Add Post
		post_time = int(time())
		logging.info("Enter name")
		name = input(": ")
		logging.info("Enter author")
		author = input(": ")
		logging.info("Enter image url")
		url = input(": ")

		post_hash = sha256(f"{author}{time}{url}".encode('utf-8')).hexdigest()

		post = {
		'name': name,
		'author': author,
		'time': post_time,
		'url': url,
		'id': post_hash[:7] # there is a pretty decent chance of a collision happening here, oh well pie!
		}

		logging.info(f"Added post {post['id']} {post['author']} {post['time']} {post['url']}")

		contents['posts'].append(post)

	elif command == 'd': # Delete post
		logging.info("Enter post id")
		post_id = input(": ")
		for p in contents['posts']:
			if p['id'] == post_id: # Id matches
				logging.info(f"Delete Post {p['id']} {p['author']} {p['url']}")
				contents['posts'].pop(contents['posts'].index(p)) # Remove post

	elif command == 'r': # Read posts
		if len(contents['posts']) == 0:
			logging.info("No posts!")
		else:
			logging.info("Displaying posts...")
			for p in contents['posts']:
				logging.info(f"ID : {p['id']}	AUTHOR: {p['author']}	IMAGE: {p['url']}")

