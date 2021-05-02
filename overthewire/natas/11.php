<?php

$defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");
$json = json_encode($defaultdata);

$encoded = 'ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw';
$json2 = base64_decode($encoded);

$outText = '';
for($i=0;$i<strlen($json2);$i++) {
  $outText .= $json[$i] ^ $json2[$i];
}

echo $outText;
echo "\n";

function xor_encrypt($in) {
    $key = 'qw8J';
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}
$mydata = array( "showpassword"=>"yes", "bgcolor"=>"#ffffff");
echo "mydata\n";
echo base64_encode(xor_encrypt(json_encode($mydata)));
echo "\n";

echo "default data\n";
echo base64_encode(xor_encrypt(json_encode($defaultdata)));
echo "\n";

?>
