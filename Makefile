.PHONY: clean test lint

TEST_PATH=./
CVERSION=code

help:
	@echo "  bot=bot_name train-nlu "
	@echo "        Train the natural language understanding using Rasa NLU."
	@echo "  bot=bot_name train-core (bot=bot_name)"
	@echo "        Train a dialogue model using Rasa core."
	@echo "  bot=bot_name port=port run "
	@echo "        Starts the bot on the command line"


run-actions:
	python3 -m rasa_core_sdk.endpoint --actions data.${CVERSION}.actions

train-nlu:
	python3 -m rasa_nlu.train -c data/${CVERSION}/nlu_tensorflow.yml --data data/$(bot)/nlu/ -o data/$(bot)/models --project $(bot) --verbose

train-core:
	python3 -m rasa_core.train -d data/$(bot)/domain.yml -s data/$(bot)/core -o data/$(bot)/models/dialogue -c data/${CVERSION}/policy.yml --debug
    
run:
	#make run-actions|  true&
	python3 -m rasa_core.run --enable_api -d data/$(bot)/models/dialogue -u data/$(bot)/models/$(bot)/$(shell ls data/$(bot)/models/$(bot) | tail -1) --port $(port) -o data/${CVERSION}/out.log --debug --endpoints data/${CVERSION}/endpoints.yml

