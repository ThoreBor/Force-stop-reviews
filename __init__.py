from aqt import mw, gui_hooks
from aqt.utils import tooltip

def force_stop_reviews(card):
	total_cards = to_learn()
	config = mw.addonManager.getConfig(__name__)

	if total_cards == config["reviews_left"]:
		tooltip(f"You now have {total_cards} cards left to review.")
		mw.moveToState("deckBrowser")

def to_learn():
	new = 0
	due = 0
	decks = mw.col.sched.deck_due_tree().children
	for deck in decks:
		new += deck.new_count
		due += deck.review_count + deck.learn_count

	return due + new

gui_hooks.reviewer_did_show_question.append(force_stop_reviews)