from aqt import mw, gui_hooks
from aqt.utils import tooltip
from aqt.overview import Overview
from anki.hooks import wrap

def force_stop_reviews(reviewer, card, ease):
	review, new = to_learn()
	config = mw.addonManager.getConfig(__name__)
	config_deck_index = active_deck_index()
	values = config["values"]

	if review == values[config_deck_index][0] or new == values[config_deck_index][1]:
		tooltip(f"You now have {review} cards left to review and {new} new cards left to learn.")
		mw.moveToState("deckBrowser")

def to_learn():
	cards = mw.col.sched.counts()
	new = cards[0]
	learn = cards[1]
	review = cards[2]
	if new == 0:
		return learn + review, None
	if learn + review == 0:
		return None, new
	if learn + review == None and new == None:
		return None, None
	else:		
		return learn + review, new

def overview_options(overview, content):
	config = mw.addonManager.getConfig(__name__)
	values = config["values"]
	config_deck_index = active_deck_index()
	due = values[config_deck_index][0]
	new = values[config_deck_index][1]
	content.table += f"""\n<div>Force stop reviews when <input type="number" id="due" value="{due}" style="width: 50px" onChange="pycmd('changeDue:'+ this.value)"> due cards, or 
	<input type="number" id="new" value="{new}" style="width: 50px" onChange="pycmd('changeNew:' + this.value)"> new cards are left in the parent deck.</div><div id="test"></div>
	"""

def overview_link_handler_wrapper(overview, url):
	config = mw.addonManager.getConfig(__name__)
	url = url.split(":")
	if url[0] == "changeDue":
		due = int(url[1])
		config_deck_index = active_deck_index()
		values = config["values"]
		values[config_deck_index] = [due, values[config_deck_index][1]]
		config = {"decks": config["decks"], "values": values}
		mw.addonManager.writeConfig(__name__, config)

	if url[0] == "changeNew":
		new = int(url[1])
		config_deck_index = active_deck_index()
		values = config["values"]
		values[config_deck_index] = [values[config_deck_index][0], new]
		config = {"decks": config["decks"], "values": values}
		mw.addonManager.writeConfig(__name__, config)

def find_decks():
	config = mw.addonManager.getConfig(__name__)
	known_decks = config["decks"]
	values = config["values"]
	decks = mw.col.decks.all()
	decklist = []
	for l in decks:
		decklist.append(l['name'])
	for i in decklist:
		if i not in known_decks and "::" not in i:
			known_decks.append(i)
			values.append([0, 0])
	config = {"decks": known_decks, "values": values}
	mw.addonManager.writeConfig(__name__, config)

def active_deck_index():
	config = mw.addonManager.getConfig(__name__)
	deck_id = mw.col.get_config("activeDecks", [1])
	current_deck = mw.col.decks.get(deck_id[0])
	current_deck = current_deck["name"]
	if "::" in current_deck:
		current_deck = current_deck.split("::")[0]
	config_deck_index = config["decks"].index(current_deck)
	return config_deck_index

Overview._linkHandler = wrap(Overview._linkHandler, overview_link_handler_wrapper, "after")

gui_hooks.reviewer_did_answer_card.append(force_stop_reviews)
gui_hooks.overview_will_render_content.append(overview_options)
gui_hooks.profile_did_open.append(find_decks)