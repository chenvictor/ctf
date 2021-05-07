#include <stdexcept>
#include <cstdlib>
#include <cstring>
#include <iostream>

#include "base64.hpp"

const std::string ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

static char mapping[256];

void gen_mapping() {
  memset(mapping, -1, sizeof(mapping));
  for (int i = 0; i < (int)ALPHABET.size(); ++i) {
    mapping[(int)ALPHABET[i]] = i;
  }
}

int get_val(char c) {
  if (c == '=') {
    return 0;
  }
  const int val = 0xff & mapping[(int)c];
  if (val == -1) {
    throw std::invalid_argument("encoded string contains invalid character");
  }
  return val;
}

/**
 * TODO check for invalid '=' padding usage
 **/

std::string base64::decode(const std::string& raw) {
  const int sz = raw.size();
  if (sz == 0) {
    return "";
  }
  const int szn = 3*sz/4;
  if (sz % 4 != 0) {
    throw std::invalid_argument("encoded string size should be multiple of 3");
  }
  if (mapping[0] == 0) {
    gen_mapping();
  }
  std::string ret(szn, '.');
  int i, j=0, val;
  for (i = 0; i < sz; i += 4) {
    val = get_val(raw[i])   << 18
        | get_val(raw[i+1]) << 12
        | get_val(raw[i+2]) << 6
        | get_val(raw[i+3]);
    ret[j++] = 0xff & (val >> 16);
    ret[j++] = 0xff & (val >> 8);
    ret[j++] = 0xff & val;
  }
  if (raw[sz-1] == '=') {
    ret.pop_back();
    if (raw[sz-2] == '=') {
      ret.pop_back();
    }
  }
  return ret;
}

std::string base64::encode(const std::string& raw) {
  const int sz = raw.size();
  if (sz == 0) {
    return "";
  }
  const int szn = ((sz-1)/3+1)*4;
  std::string ret(szn, 0);
  int i, j = 0, val;
  for (i = 0; i < sz; i += 3) {
    val = ((raw[i] & 0xff) << 16)
        | ((i+1 < sz) ? (raw[i+1] & 0xff) << 8 : 0)
        | ((i+2 < sz) ? (raw[i+2] & 0xff) : 0);
    ret[j++] = ALPHABET[0x3f & (val >> 18)];
    ret[j++] = ALPHABET[0x3f & (val >> 12)];
    ret[j++] = ALPHABET[0x3f & (val >> 6)];
    ret[j++] = ALPHABET[0x3f & val];
  }
  const int rem = sz % 3;
  if (rem) {
    ret[szn-1] = '=';
    if (rem == 1) {
      ret[szn-2] = '=';
    }
  }
  return ret;
}

