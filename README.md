# metadonneHive

This python script allows you to detect all the type of an hive database table exported without any metadonne attached.
He will extract methadonne from thoses exported hive table.
Put it in a directory with all yout undefined tables dumped and launche it, it will generate all the sql queries to create Hive's metadonne suitable to your databases.

* type supported
- STRING
- DATE (yyyy-mm-dd hh:mm:ss), timestamp form
- FLOAT
- BIG INT
- INT

* separators supported (you can add other ones on the begining of the script
- ;
- tabulation

Have fun !
