#include <ncurses.h>
#include <signal.h>

#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

#include "base64.hpp"
#include "freq.hpp"

using char8_t = unsigned char;

std::string key;
std::vector<std::string> lines;

int ymax, xmax; // screen size limit
int ypos, xpos; // current cursor position
int yscr, xscr; // current scroll position
int ylim, xlim; // line count and maximum line size

void show_status();
void show_lines(int xonly=-1);
chtype get_display_ch(char c);
void rmove(int dy, int dx);

void set_key(int pos, int k) {
  key.at(pos) = k;
  show_lines(pos-xscr);
}

void update_key(int pos, char c, bool advance_cursor=true) {
  const std::string& line = lines[ypos];
  if (pos >= (int)line.size()) {
    return;
  }
  set_key(pos, c ^ line[pos]);
  if (advance_cursor) {
    rmove(0, +1);
  }
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
  show_status();
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
  ymax--;

  // move to initial (0,0) position
  ypos = xpos = 0;
  yscr = xscr = 0;
  rmove(0, 0);
}

void my_exit() {
  endwin();
  // output base64 encoded result
  for (std::string& line : lines) {
    std::transform(line.begin(), line.end(), key.begin(), line.begin(), std::bit_xor());
    std::cout << base64::encode(line) << '\n';
  }
  std::cout.flush();
}

bool is_printable(char c) {
  return 32 <= c && c < 127;
}

char get_ch(const std::string& s, int pos) {
  if (pos >= (int)s.size()) {
    return ' ';
  }
  return s.at(pos) ^ key[pos];
}

chtype get_display_ch(char c) {
  if (is_printable(c)) {
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
  int xlow = 0, xhigh = std::min(xlim-xscr, xmax);
  if (xonly != -1){
    xlow = xonly;
    xhigh = xlow + 1;
  }
  for (int y = 0; y < std::min(ylim-yscr, ymax); ++y) {
    wmove(stdscr, y, xlow);
    const std::string& line = lines[y+yscr];
    for (int x = xlow; x < xhigh; ++x) {
      const char c = get_ch(line, x+xscr);
      chtype dchar = get_display_ch(c);
      assert(addch(dchar) != ERR);
    }
  }
  rmove(0, 0);
}

/**
 * Status bar display
 **/
void show_status() {
  const std::string& line = lines[ypos];
  wmove(stdscr, ymax, 0);
  clrtoeol();
  if (xpos >= (int)line.size()) {
    printw("no char");
  } else {
    const char c = get_ch(line, xpos);
    printw("Hex: 0x%02x  Dec: %3d", 0xff & c, 0xff & c);
  }
  rmove(0, 0);
}

void solve() {
  for (int x = 0; x < xlim; ++x) {
    std::pair<long long,int> best(std::numeric_limits<long long>::min(), 0);
    for (int k = 0; k < 256; ++k) {
      long long score = 0;
      for (const std::string& line : lines) {
        if (x >= (int)line.size()) continue;
        score += freq::score_letter(0xff & (line[x] ^ k));
      }
      best = max(best, std::make_pair(score, k));
    }
    set_key(x, best.second);
  }
}

int main(int argc, char** argv) {
  read_input();

  my_init();
  atexit(my_exit);

  show_lines();
  show_status();

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
        break;
      case '\n':
        solve();
        break;
      default:
        if (is_printable(ch)) {
          update_key(xpos, ch);
        }
    }
  }
  return 0;
}

