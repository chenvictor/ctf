#include <ncurses.h>
#include <signal.h>

#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include "base64.hpp"

using char8_t = unsigned char;

std::string key;
std::vector<std::string> lines;

int ymax, xmax; // screen size limit
int ypos, xpos; // current cursor position
int yscr, xscr; // current scroll position
int ylim, xlim; // line count and maximum line size

void show_lines(int xonly=-1);
chtype get_display_ch(const std::string& s, int pos);

void update_key(char c) {
  const std::string& line = lines[ypos];
  if (xpos >= (int)line.size()) {
    return;
  }
  key.at(xpos) = c ^ line[xpos];
  show_lines(xpos);
}

bool update_scroll(int& dscr, int dpos, int dmax) {
  if (dpos < dscr) {
    dscr = dpos;
    return true;
  } else if (dpos - dmax >= dscr) {
    dscr = dpos - dmax + 1;
    return true;
  }
  return false;
}

void rmove(int dy, int dx) {
  const int ynew = std::clamp(ypos + dy, 0, ylim-1);
  const int xnew = std::clamp(xpos + dx, 0, xlim-1);
  dy = ynew - ypos;
  dx = xnew - xpos;
  ypos = ynew;
  xpos = xnew;
  wmove(stdscr, ypos-yscr, xpos-xscr);
  if (dy == 0 && dx == 0) return;
  const bool yscrolled = update_scroll(yscr, ypos, ymax);
  const bool xscrolled = update_scroll(xscr, xpos, xmax);
  if (yscrolled || xscrolled) {
    show_lines();
  }
}

void read_input() {
  xlim = 0;
  std::string line;
  while (getline(std::cin,line)) {
    lines.emplace_back(base64::decode(line));
    xlim = std::max(xlim, (int)lines.back().size());
  }
  ylim = lines.size();
  key.resize(xlim);
}

void on_sigint(int signum) {
  exit(0);
}

void my_init() {
  signal(SIGINT, on_sigint);

  // ncurses setup
  FILE *f = fopen("/dev/tty", "r+");
  SCREEN *screen = newterm(NULL, f, f);
  set_term(screen);
  cbreak();
  noecho();
  keypad(stdscr, TRUE);
  getmaxyx(stdscr, ymax, xmax);

  // move to initial (0,0) position
  ypos = xpos = 0;
  yscr = xscr = 0;
  rmove(0, 0);
}

void my_exit() {
  endwin();
  // output base64 encoded result
  for (const std::string& line : lines) {
    std::cout << base64::encode(line) << '\n';
  }
  std::cout.flush();
}

bool is_printable(char c) {
  return 32 <= c && c < 127;
}

chtype get_display_ch(const std::string& s, int pos) {
  if (pos >= (int)s.size()) {
    return ' ';
  }
  const char c = s[pos] ^ key[pos];
  if (is_printable(c)) {
    // printable char
    return c;
  }
  // odd whitespace
  switch (c) {
    case '\t':
    case '\n':
      return ACS_BULLET;
  }
  // otherwise, non-printable
  return ACS_DIAMOND;
}

void show_lines(int xonly) {
  // TODO only re-render xonly?
  for (int y = 0; y < std::min(ylim-yscr, ymax); ++y) {
    wmove(stdscr, y, 0);
    const std::string& line = lines[y+yscr];
    for (int x = 0; x < std::min(xlim-xscr, xmax); ++x) {
      chtype dchar = get_display_ch(line, x+xscr);
      assert(addch(dchar) != ERR);
    }
  }
  rmove(0, 0);
}

int main(int argc, char** argv) {
  read_input();

  my_init();
  atexit(my_exit);

  show_lines();

  while(1) {
    const int ch = getch();
    switch (ch) {
      case KEY_LEFT:
        rmove(0, -1);
        break;
      case KEY_RIGHT:
        rmove(0, +1);
        break;
      case KEY_UP:
        rmove(-1, 0);
        break;
      case KEY_DOWN:
        rmove(+1, 0);
      default:
        if (is_printable(ch)) {
          update_key(ch);
        }
    }
  }

  return 0;
}

