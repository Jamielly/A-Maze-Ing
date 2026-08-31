# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jamielly-reis <jamielly-reis@student.42    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/08/31 12:11:38 by jamielly-re       #+#    #+#              #
#    Updated: 2026/08/31 12:26:35 by jamielly-re      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

PYTHON = python3
PIP = pip3
MAIN = a_maze_ing.py
CONFIG = config.txt

.PHONY: all install run debug clean fclean lint lint-strict build test

all: run

install:
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy build

run: $(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache build dist *.egg-info
	find . -type d -name "_pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

fclean: clean
	rm -f output_maze.txt maze.txt
	rm -f mazegen-*.whl mazegen-*.tar.gz

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

build: clean
	$(PYTHON) -m build --sdist --wheel --outdir .

test: 
	@if [ -f maze_analyzer.py ] && [ -f output_maze.txt ]; then \
		$(PYTHON) maze_analyzer.py output_maze.txt; \
	elif [ -f maze_analyzer2.txt ] && [ -f output_maze.txt ]; then \
		$(PYTHON) maze_analyzer2.txt output_maze.txt; \
	else \
		echo "Execute o programa primeiro (make run) para gerra o output_maze.txt"; \
	fi