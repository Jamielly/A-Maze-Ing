# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jamielly-reis <jamielly-reis@student.42    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/09/15 19:29:27 by jamsilva          #+#    #+#              #
#    Updated: 2026/09/15 19:31:12 by jamielly-re      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME        := mazegen
MAIN        := a_maze_ing.py
CONFIG      := config.txt

PYTHON      := python3
VENV        := .venv
PYTHON_VENV := $(VENV)/bin/python
PIP         := $(PYTHON_VENV) -m pip

BUILD_DIR   := build
DIST_DIR    := dist
TEST_ENV    := .testenv

PIP_INDEX   ?= https://pypi.org/simple

DEV_TOOLS := \
	flake8 \
	mypy \
	build \
	setuptools \
	wheel

MYPY_FLAGS := \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

RESET  := \033[0m
GREEN  := \033[32m
YELLOW := \033[33m
BLUE   := \033[34m
RED    := \033[31m
CYAN   := \033[36m

.PHONY: all help install venv check run debug \
        lint lint-strict \
        package package-check \
        clean fclean re

all: check run

help:
	@printf "\n$(CYAN)A-Maze-ing / mazegen$(RESET)\n"
	@printf "$(CYAN)====================$(RESET)\n\n"
	@printf "Usage:\n\n"
	@printf "  $(GREEN)make install$(RESET)        Create/update development environment\n"
	@printf "  $(GREEN)make check$(RESET)          Run all static checks\n"
	@printf "  $(GREEN)make run$(RESET)            Generate the maze\n"
	@printf "  $(GREEN)make debug$(RESET)          Run with Python PDB\n"
	@printf "  $(GREEN)make lint$(RESET)           Run Flake8 + Mypy\n"
	@printf "  $(GREEN)make lint-strict$(RESET)   Run Flake8 + Mypy --strict\n"
	@printf "  $(GREEN)make package$(RESET)        Build wheel + source distribution\n"
	@printf "  $(GREEN)make package-check$(RESET)  Build and validate distributions\n"
	@printf "  $(GREEN)make clean$(RESET)          Remove caches\n"
	@printf "  $(GREEN)make fclean$(RESET)         Remove all generated files\n"
	@printf "  $(GREEN)make re$(RESET)             Full rebuild\n"
	@printf "\n"

venv: $(PYTHON_VENV)

$(PYTHON_VENV):
	@printf "$(BLUE)→ Creating virtual environment...$(RESET)\n"
	$(PYTHON) -m venv $(VENV)
	@printf "$(GREEN)✓ Virtual environment created.$(RESET)\n"

install: venv
	@printf "$(BLUE)→ Updating pip...$(RESET)\n"
	$(PIP) install --index-url $(PIP_INDEX) --upgrade pip

	@printf "$(BLUE)→ Installing development tools...$(RESET)\n"
	$(PIP) install --index-url $(PIP_INDEX) $(DEV_TOOLS)

	@printf "$(GREEN)✓ Development environment ready.$(RESET)\n"

check: lint

lint: venv
	@printf "$(BLUE)→ Running Flake8...$(RESET)\n"
	$(PYTHON_VENV) -m flake8 .

	@printf "$(BLUE)→ Running Mypy...$(RESET)\n"
	$(PYTHON_VENV) -m mypy . $(MYPY_FLAGS)

	@printf "$(GREEN)✓ Static analysis passed.$(RESET)\n"

lint-strict: venv
	@printf "$(BLUE)→ Running Flake8...$(RESET)\n"
	$(PYTHON_VENV) -m flake8 .

	@printf "$(BLUE)→ Running Mypy --strict...$(RESET)\n"
	$(PYTHON_VENV) -m mypy . --strict

	@printf "$(GREEN)✓ Strict static analysis passed.$(RESET)\n"

run:
	@test -f "$(MAIN)" || \
		(printf "$(RED)✗ Missing $(MAIN).$(RESET)\n" && exit 1)

	@test -f "$(CONFIG)" || \
		(printf "$(RED)✗ Missing $(CONFIG).$(RESET)\n" && exit 1)

	@printf "$(BLUE)→ Running $(MAIN)...$(RESET)\n"
	$(PYTHON) $(MAIN) $(CONFIG)

	@printf "$(GREEN)✓ Execution completed.$(RESET)\n"

debug:
	@test -f "$(MAIN)" || \
		(printf "$(RED)✗ Missing $(MAIN).$(RESET)\n" && exit 1)

	@test -f "$(CONFIG)" || \
		(printf "$(RED)✗ Missing $(CONFIG).$(RESET)\n" && exit 1)

	@printf "$(YELLOW)→ Starting PDB debugger...$(RESET)\n"
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

package: install clean
	@printf "$(BLUE)→ Building $(NAME)...$(RESET)\n"
	$(PYTHON_VENV) -m build

	@printf "$(GREEN)✓ Distribution created in ./$(DIST_DIR)/$(RESET)\n"
	@ls -lh $(DIST_DIR)

package-check: package
	@set -e; \
	printf "\n$(CYAN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)\n"; \
	printf "$(CYAN) Testing wheel$(RESET)\n"; \
	printf "$(CYAN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)\n"; \
	rm -rf "$(TEST_ENV)"; \
	$(PYTHON) -m venv "$(TEST_ENV)"; \
	"$(TEST_ENV)/bin/python" -m pip install \
		--index-url "$(PIP_INDEX)" \
		$(DIST_DIR)/$(NAME)-*.whl; \
	cd /tmp; \
	"$(CURDIR)/$(TEST_ENV)/bin/python" -c \
		"from mazegen import MazeGenerator; \
		m = MazeGenerator(20, 20, (0, 0), (19, 19), seed=42, perfect=True); \
		m.generate(); \
		print('WHL OK:', m is not None)"; \
	rm -rf "$(CURDIR)/$(TEST_ENV)"

	@set -e; \
	printf "\n$(CYAN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)\n"; \
	printf "$(CYAN) Testing source distribution$(RESET)\n"; \
	printf "$(CYAN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)\n"; \
	rm -rf "$(TEST_ENV)"; \
	$(PYTHON) -m venv "$(TEST_ENV)"; \
	"$(TEST_ENV)/bin/python" -m pip install \
		--index-url "$(PIP_INDEX)" \
		$(DIST_DIR)/$(NAME)-*.tar.gz; \
	cd /tmp; \
	"$(CURDIR)/$(TEST_ENV)/bin/python" -c \
		"from mazegen import MazeGenerator; \
		m = MazeGenerator(20, 20, (0, 0), (19, 19), seed=42, perfect=True); \
		m.generate(); \
		print('SDIST OK:', m is not None)"; \
	rm -rf "$(CURDIR)/$(TEST_ENV)"

	@printf "\n$(GREEN)✓ All distributions passed validation.$(RESET)\n"

clean:
	@printf "$(BLUE)→ Removing Python caches...$(RESET)\n"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

	@printf "$(GREEN)✓ Cache cleanup complete.$(RESET)\n"

fclean: clean
	@printf "$(BLUE)→ Removing build artifacts...$(RESET)\n"
	rm -rf $(BUILD_DIR)
	rm -rf $(DIST_DIR)
	rm -rf $(VENV)
	rm -rf $(TEST_ENV)
	rm -rf *.egg-info
	rm -f $(NAME)-*.whl
	rm -f $(NAME)-*.tar.gz

	@printf "$(GREEN)✓ Full cleanup complete.$(RESET)\n"

re: fclean
	@printf "$(CYAN)→ Rebuilding project...$(RESET)\n"
	$(MAKE) all
