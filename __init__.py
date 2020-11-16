from aqt import mw, gui_hooks
from aqt.utils import tooltip

def force_stop_reviews(card):
	config = mw.addonManager.getConfig(__name__)
	currently = config["current_reviews"]
	currently += 1
	config = {"max_reviews": config["max_reviews"], "current_reviews": currently}
	mw.addonManager.writeConfig(__name__, config)

	if currently >= config["max_reviews"]:
		tooltip(f"You reviewed {currently} cards.")
		mw.moveToState("deckBrowser")
		config = {"max_reviews": config["max_reviews"], "current_reviews": 0}
		mw.addonManager.writeConfig(__name__, config)

gui_hooks.reviewer_did_show_question.append(force_stop_reviews)