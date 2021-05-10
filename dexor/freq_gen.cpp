#include <array>
#include <iostream>
#include <string>

/**
 * Generated using frequencies from
 * https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
 **/

constexpr int CHAR_LIM = 256;
#define SF(s,v) set_freq(s,v)

std::array<int,CHAR_LIM> freq_map;

void set_freq(std::string s, int val) {
  for (char c : s) {
    freq_map[c] = val;
  }
}

int main() {
  // generate
  freq_map.fill(-1e4);
  SF("eE", 120);
  SF("tT", 90);
  SF("ainosAINOS", 80);
  SF("hH", 64);
  SF("rR", 62);
  SF("dD", 44);
  SF("lL", 40);
  SF("uU", 34);
  SF("cmCM", 30);
  SF("fF", 25);
  SF("wyWY", 20);
  SF("gpGP", 17);
  SF("bB", 16);
  SF("vV", 12);
  SF("kK", 8);
  SF("qQ", 5);
  SF("jxJX", 4);
  SF("zZ", 2);

  SF(" ", 100);
  SF(".,;", 20);
  SF("!?@-+'\"", 0);

  // print
  for (int i = 0; i < CHAR_LIM; ++i) {
    printf("%d, ", freq_map[i]);
    if (i % 8 == 7) {
      printf("\n");
    }
  }
}

