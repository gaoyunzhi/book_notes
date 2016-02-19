#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
class NoteWriter:
	def __init__(self, content):
		self.content = content.decode('utf-8')
		self.notes_index = []

	def add(self, note):
		self.current_note = note.decode('utf-8')
		in_block = False
		self.start_index = None
		note_index = None
		for index, char in enumerate(self.current_note): 
			if ord(char) < 128 or char in [u'“']:
				in_block = False
				continue
			if in_block:
				continue
			self.try_find_anchor(index)
			if self.start_index >= 0:
				note_index = index
				break
			in_block = True
		if note_index == None:
			return # no find
		content_index = self.start_index + len(self.anchor) - 1
		self.end_index = content_index
		grace_space = 10
		last_grace_space = 0
		for index in xrange(note_index + len(self.anchor), len(self.current_note)):
			char = self.current_note[index]
			if ord(char) < 128:
				grace_space += 1
				continue
			current_content_index = \
				self.content.find(char, content_index - last_grace_space + 1)
			if current_content_index == -1 or 
				current_content_index - content_index > grace_space:
				continue
			last_grace_space = current_content_index - content_index - 1
			if last_grace_space == 0:
				self.end_index = current_content_index
			content_index = current_content_index
			grace_space = 10	
		user_note = [] 
		for char in self.current_note[self.end_index:]:
			if ord(char) < 128:
				continue
			user_note.append(char)
		self.notes_index.append(
			[self.start_index, self.end_index, "".join(user_note)])

	def try_find_anchor(self, note_index):
		end_index = note_index + 1
		while True:
			occurence = self.findNum(self.current_note[note_index: end_index + 1])
			if occurence > 1:
				end_index += 1
				continue
			if occurence == 0:
				break
			if occurence == 1:
				end_index += 1
				break
		if end_index - note_index <= 1:
			return
		self.anchor = self.current_note[note_index: end_index]
		self.start_index = self.content.find(self.anchor)

	def findNum(self, anchor):
		index_1 = self.content.find(anchor)
		if index_1 == -1:
			return 0
		index_2 = self.content.find(anchor, index_1 + 1)
		if index_2 == -1:
			return 1
		return 2 # ok, this function is actually not find occurence, but just to
		# distinguish the case between 0, 1 and >= 2

	def getContentWithNotes(self):
		self.notes_index.sort()
		pre_start = None
		pre_end = 0
		pre_note = ""
		new_notes_index = []
		user_notes = []
		for start, end, note in self.notes_index:
			if pre_end >= start:
				pre_end = end
			else:
				if pre_start != None:
					new_notes_index.append([pre_start, pre_end, pre_note])
				pre_start = start
				pre_end = end
				pre_note = note
		if pre_start != None:
			new_notes_index.append([pre_start, pre_end, pre_note])
		splitted_contents = []
		pre_end = 0
		for start, end, note in new_notes_index:
			splitted_contents.append(self.content[pre_end :start])
			splitted_contents.append('<b class="calibre_1001">')
			splitted_contents.append(self.content[start: end + 1])
			pre_end = end + 1
			splitted_contents.append('</b><span class="calibre_1002">')
			splitted_contents.append(note)
			splitted_contents.append('</span>')
		splitted_contents.append(self.content[pre_end:])
		return "".join(splitted_contents).encode('utf-8')

def insert_notes(notes, tmp_dir):
	index_file_handle = open(os.path.join(tmp_dir, 'index.html'), 'r')
	content = index_file_handle.read()
	index_file_handle.close()
	
	note_writer = NoteWriter(content)
	for note in notes:
		note_writer.add(note)

	index_file_handle = open(os.path.join(tmp_dir, 'index.html'), 'w')
	index_file_handle.write(note_writer.getContentWithNotes())
	index_file_handle.close()
	
	css_file_handle = open(os.path.join(tmp_dir, 'style.css'), 'a')
	css_file_handle.write('.calibre_1001 { text-decoration: underline; text-decoration-style: dotted;}\n')
	css_file_handle.write('.calibre_1002 { font-size: 60%;}')
	css_file_handle.close()