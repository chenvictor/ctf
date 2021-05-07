#ifndef __BASE64__
#define __BASE64__

#include <string>

namespace base64 {
  std::string decode(const std::string& raw);
  std::string encode(const std::string& raw);
}

#endif // BASE64

