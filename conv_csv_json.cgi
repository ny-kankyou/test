#!/usr/bin/perl

#use utf8;
#use Encode;
use CGI;
use Jcode;
use Archive::Zip;

my ($query,$filename);
$query = new CGI;
$filename = $query->param('file');

if (! $filename) {
print "Content-Type: text/html; charset=UTF-8\n\n";
print <<HTML;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>ERR</title>
</head>
<body>
<h1>CSVファイルを選択してください。</h1>

</body>
</html>
HTML
exit;
}

while (read($filename, $buffer, 2048)) { $file .= $buffer; }
if (getcode("$file") !~ /utf8/i) {
#	$file = decode('utf-8', $file);
	$file = Jcode::convert( $file , "utf-8" );
}


$tmpfile = time . $$;
open(OUT, "> ./FILE/$tmpfile");
print OUT "$file";
close(OUT);

#テンプレートフォルダの内容をコピーする
`rm -r ./copy/*`;
`cp -r ./tmp/* ./copy/`;



#print "Content-Type: text/html; charset=UTF-8\n\n";
#print getcode("$file");

#print "Content-Type: text/html\n\n";
#print $filename;
#print $file;

=pod
No.
質問内容
答え
質問言い換え１
質問言い換え２
質問言い換え３
LINE文章
LINE画像（URL）
LINE選択肢タイトル
LINE選択肢1
LINE選択肢2
LINE選択肢3
LINE画像選択肢タイトル
サブタイトル
画像URL
ボタン１テキスト
ボタン１ポスト
ボタン２テキスト
ボタン２ポスト
ボタン３テキスト
ボタン３ポスト
Custom
=cut

#print "Content-Type: text/html; charset=UTF-8\n\n";

open(DATA, "./FILE/$tmpfile");
while (my $line = <DATA>) {
  $line .= <DATA> while ($line =~ tr/"// % 2 and !eof(DATA));

  $line =~ s/(?:\x0D\x0A|[\x0D\x0A])?$/,/;
  @row = map {/^"(.*)"$/s ? scalar($_ = $1, s/""/"/g, $_) : $_}
                ($line =~ /("[^"]*(?:""[^"]*)*"|[^,]*),/g);

#print join(',',@row) . "<br>\n";

#項目名をAIで取得する
if (! $bit) {
$i = 0;
foreach my $k (@row) {
if ($k =~ /(custom|カスタム|json)/i) {$L[21] = $i;}
elsif ($k =~ /(3|３)(ポスト|post)/i || $k =~ /(ポスト|post)(3|３)/i) {$L[20] = $i;}
elsif ($k =~ /(3|３)(テキスト|text|txt)/i || $k =~ /(テキスト|text|txt)(3|３)/i) {$L[19] = $i;}
elsif ($k =~ /(2|２)(ポスト|post)/i || $k =~ /(ポスト|post)(2|２)/i) {$L[18] = $i;}
elsif ($k =~ /(2|２)(テキスト|text|txt)/i || $k =~ /(テキスト|text|txt)(2|２)/i) {$L[17] = $i;}
elsif ($k =~ /(1|１)(ポスト|post)/i || $k =~ /(ポスト|post)(1|１)/i) {$L[16] = $i;}
elsif ($k =~ /(1|１)(テキスト|text|txt)/i || $k =~ /(テキスト|text|txt)(1|１)/i) {$L[15] = $i;}
elsif ($k =~ /画像/ && $k =~ /(URL|ｕｒｌ|ＵＲＬ)/i) {$L[14] = $i;}
elsif ($k =~ /(サブタイトル|sub.*title)/i) {$L[13] = $i;}
elsif ($k =~ /画像選択肢(タイトル|title)/i) {$L[12] = $i;}
elsif ($k =~ /選択肢(3|３)/i) {$L[11] = $i;}
elsif ($k =~ /選択肢(2|２)/i) {$L[10] = $i;}
elsif ($k =~ /選択肢(1|１)/i) {$L[9] = $i;}
elsif ($k =~ /選択肢(タイトル|title)/i) {$L[8] = $i;}
elsif ($k =~ /(LINE|ライン|ＬＩＮＥ).*画像/i) {$L[7] = $i;}
elsif ($k =~ /(LINE|ライン|ＬＩＮＥ).*(文章|テキスト|txt)/i) {$L[6] = $i;}
elsif ($k =~ /言.*(換|替|代|変).*(3|３)/) {$L[5] = $i;}
elsif ($k =~ /言.*(換|替|代|変).*(2|２)/) {$L[4] = $i;}
elsif ($k =~ /言.*(換|替|代|変).*(1|１)/) {$L[3] = $i;}
elsif ($k =~ /(答|ans)/i || $k =~ /(A|Ａ|ａ)$/i) {$L[2] = $i;}
elsif ($k =~ /質問/ || $k =~ /(Q|Ｑ|ｑ)$/i) {$L[1] = $i;}
elsif ($k =~ /(no|ＮＯ|番号)/i) {$L[0] = $i;}
$i++;
}
$bit = 1;
next;
}



#print "S:$L[1]=" . $row[$L[1]] . ",$L[2]=" . $row[$L[2]] . "<br>\n";
#next;


#質問も答えも無ければ何もしない
if (! defined($L[1]) || ! defined($L[2])) {
print "Content-Type: text/html; charset=UTF-8\n\n";
print <<HTML;
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>ERR</title>
</head>
<body>
<h1>「質問」と「答え」は必須項目です。</h1>
</body>
</html>
HTML
exit;
}


if (! $row[$L[1]]) {next;}
$row[$L[1]] =~ s/\s//g;


open(JSON1, "> ./copy/intents/" . $row[$L[1]] . ".json");

		# Flag 2020.03.21追加
		$LineFlag = 0;

		# intentsファイル
		#id = "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(4)])) + "-" +"".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(6)]))
		print JSON1 "{\n";
		print JSON1 "\t\"id\" : \"" . &create_id . "\",\n";
		print JSON1 "\t\"name\" : \"$row[$L[1]]\",\n";
		print JSON1 "\t\"auto\" : true,\n";
		print JSON1 "\t\"contexts\" : [],\n";
		print JSON1 "\t\"responses\" : [\n";
		print JSON1 "\t\t{";
		print JSON1 "\t\t\"resetContexts\": false,\n";
		print JSON1 "\t\t\"affectedContexts\": [],\n";
		print JSON1 "\t\t\"parameters\": [],\n";
		print JSON1 "\t\t\"messages\": [\n";		#2020.09.11変更 ,を削除
		print JSON1 "\t\t\t{\n";			# 通常メッセージの始まり
		print JSON1 "\t\t\t\"type\" : 0, \"lang\" : \"ja\", \"speech\" : \"$row[$L[2]]\"\n";
		print JSON1 "\t\t\t},{\n";
		print JSON1 "\t\t\t\"type\" : 0, \"lang\" : \"ja\", \"speech\" : []\n";

		# LINE用に追加するならこの行の次に入れる
		if (defined($L[6]) && $row[$L[6]]) {			# LINE用の文字列
			$LineFlag = 1;
			print JSON1 "\t\t\t},{\n";
			print JSON1 "\t\t\t\"type\" : 0, \"platform\" : \"line\", \"lang\" : \"ja\", \"speech\" : \"$row[$L[6]]\"\n";
		}
		if (defined($L[7]) && $row[$L[7]]) {			# LINE用の画像
			$LineFlag = 1;
			print JSON1 "\t\t\t},{\n";
			print JSON1 "\t\t\t\"type\" : 3, \"platform\" : \"line\", \"lang\" : \"ja\", \"imageUrl\" : \"$row[$L[7]]\"\n";
		}
		if (defined($L[8]) && $row[$L[8]]) {			# LINE用のボタン型選択肢
			$LineFlag = 1;
			print JSON1 "\t\t\t},{\n";
			print JSON1 "\t\t\t\"type\" : 2, \"platform\" : \"line\", \"lang\" : \"ja\", \"title\" : \"$row[$L[8]]\", \"replies\" : [";
			if (defined($L[9]) && $row[$L[9]]) {			# LINE用のボタン型選択肢
				print JSON1 "\"$row[$L[9]]\"";
			}
			if (defined($L[10]) && $row[$L[10]]) {			# LINE用のボタン型選択肢
				print JSON1 ",\"$row[$L[10]]\"";
			}
			if (defined($L[11]) && $row[$L[11]]) {			# LINE用のボタン型選択肢
				print JSON1 ",\"$row[$L[11]]\"";
			}
			print JSON1 "]\n";
		}

		if (defined($L[12]) && $row[$L[12]]) {			# LINE用の画像付きボタン
			$LineFlag = 1;
			print JSON1 "\t\t\t},{\n";
			print JSON1 "\t\t\t\"type\" : 1, \"platform\" : \"line\", \"lang\" : \"ja\", \"title\" : \"$row[$L[12]]\" , \"subtitle\" : \"$row[$L[13]]\" , \"imageUrl\" : \"$row[$L[14]]\" , \"buttons\" : [";
			if (defined($L[15]) && $row[$L[15]]) {			# LINE用のボタン型選択肢
				print JSON1 "{\"text\" : \"$row[$L[15]]\"";
				if (defined($L[16]) && $row[$L[16]]) {			# LINE用のボタン型選択肢
					print JSON1 ",\"postback\" : \"$row[$L[16]]\"";
				}
				print JSON1 "}";
			}
			if (defined($L[17]) && $row[$L[17]]) {				# LINE用のボタン型選択肢
				print JSON1 ",{\"text\" : \"$row[$L[17]]\"";
				if (defined($L[18]) && $row[$L[18]]) {			# LINE用のボタン型選択肢
					print JSON1 ",\"postback\" : \"$row[$L[18]]\"";
				}
				print JSON1 "}";
			}
			if (defined($L[19]) && $row[$L[19]]) {				# LINE用のボタン型選択肢
				print JSON1 ",{\"text\" : \"$row[$L[19]]\"";
				if (defined($L[20]) && $row[$L[20]]) {			# LINE用のボタン型選択肢
					print JSON1 ",\"postback\" : \"$row[$L[20]]\"";
				}
				print JSON1 "}";
			}
			print JSON1 "]\n";
		}
		if (defined($L[21]) && $row[$L[21]]) {			# LINE用のCustom
			$LineFlag = 1;
			print JSON1 "\t\t\t},{\n";
			print JSON1 "\t\t\t\"type\" : 4, \"platform\" : \"line\", \"lang\" : \"ja\", \"payload\" : { \"line\" : $row[$L[21]] }";
		}

		# LINE用終わり
		print JSON1 "\t\t\t}\n\t\t],\n";
		if ($LineFlag > 0) {
			print JSON1 "\t\t\"defaultResponsePlatforms\" : {},\n";
		} else {
			print JSON1 "\t\t\"defaultResponsePlatforms\" : {\"line\": true},\n";
		}
		print JSON1 "\t\t\"speech\" : []\n";
		print JSON1 "\t\t}\n\t],\n";
		print JSON1 "\t\"priority\": 500000, \"webhookUsed\" : false, \"webhookForSlotFilling\" : false, \"lastUpdate\" : 20190102, \"fallbackIntent\" : false, \"events\": []\n";
		print JSON1 "}\n";

close(JSON1);




open(JSON2, "> ./copy/intents/" . $row[$L[1]] . "_usersays_ja.json");

		#intentsのTraining pharaases
		#id = "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(4)])) + "-" +"".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(6)]))
		print JSON2 "[\n\t{\n";
		print JSON2 "\t\t\"id\" : \"" . &create_id . "\",\n";
		print JSON2 "\t\t\"data\" : [\n\t\t\t{\n";
		print JSON2 "\t\t\t\"text\" : \"$row[$L[1]]\",\n";
		print JSON2 "\t\t\t\"userDefined\" : false\n";
		print JSON2 "\t\t\t}\n\t\t],\n";
		print JSON2 "\t\t\"isTemplate\": false, \"count\" : 0, \"updated\" : 20190102\n";
		print JSON2 "\t}";

		if (defined($L[3]) && $row[$L[3]]) {		#別の言い方
			#id = "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(4)])) + "-" +"".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(6)]))
			print JSON2 "\n\t,{\n";
			print JSON2 "\t\t\"id\" : \"" . &create_id . "\",\n";
			print JSON2 "\t\t\"data\" : [\n\t\t\t{\n";
			print JSON2 "\t\t\t\"text\" : \"$row[$L[3]]\",\n";
			print JSON2 "\t\t\t\"userDefined\" : false\n";
			print JSON2 "\t\t\t}\n\t\t],\n";
			print JSON2 "\t\t\"isTemplate\": false, \"count\" : 0, \"updated\" : 20190102\n";
			print JSON2 "\t}\n";
		}
		if (defined($L[4]) && $row[$L[4]]) {		#別の言い方
			#id = "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(4)])) + "-" +"".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(6)]))
			print JSON2 "\n\t,{\n";
			print JSON2 "\t\t\"id\" : \"" . &create_id . "\",\n";
			print JSON2 "\t\t\"data\" : [\n\t\t\t{\n";
			print JSON2 "\t\t\t\"text\" : \"$row[$L[4]]\",\n";
			print JSON2 "\t\t\t\"userDefined\" : false\n";
			print JSON2 "\t\t\t}\n\t\t],\n";
			print JSON2 "\t\t\"isTemplate\": false, \"count\" : 0, \"updated\" : 20190102\n";
			print JSON2 "\t}\n";
		}
		if (defined($L[5]) && $row[$L[5]]) {		#別の言い方
			#id = "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(4)])) + "-" +"".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(6)]))
			print JSON2 "\n\t,{\n";
			print JSON2 "\t\t\"id\" : \"" . &create_id . "\",\n";
			print JSON2 "\t\t\"data\" : [\n\t\t\t{\n";
			print JSON2 "\t\t\t\"text\" : \"$row[$L[5]]\",\n";
			print JSON2 "\t\t\t\"userDefined\" : false\n";
			print JSON2 "\t\t\t}\n\t\t],\n";
			print JSON2 "\t\t\"isTemplate\": false, \"count\" : 0, \"updated\" : 20190102\n";
			print JSON2 "\t}\n";
		}

		print JSON2 "\n]\n";


close(JSON2);


#print "S:$L[1]=" . $row[$L[1]] . ",$L[2]=" . $row[$L[2]] .  ",$L[4]=" . $row[$L[4]] . "<br>\n";
#next;



}
close(DATA);


#exit;
#出来たディレクトリーとファイルを圧縮する
$zip=Archive::Zip->new;
$zip->addTree('./copy/intents','intents');
$zip->addFile('./copy/agent.json','agent.json');
$zip->addFile('./copy/package.json','package.json');
$zip->writeToFileNamed('nayoro-city-bot.zip');

print "Content-Type: application/force-download\n";
print "Content-disposition: attachment; filename=\"nayoro-city-bot.zip\"\n\n";



open(ZIP, "./nayoro-city-bot.zip");
binmode(ZIP);
while (<ZIP>) { print; }
close(ZIP);




#idを作る（とりあえずユニークに）
sub create_id {
#$iii++;
#my $id = time . sprintf("-A%07d", $iii);
my $id = `uuidgen`;	#ユニークなid　UUID をLinuxコマンドで作成 2020.09.11
$id =~ s/(\n|\r)//g;
return $id;
}




exit;

__END__

# coding:utf-8
# 市川博之（Hiroyuki Ichikawa） 2019/5/3
# var 1.10 LINE用の基本コマンド対応
#
#
import csv
import random
import sys

args = sys.argv

filename = './' + args[1]

with open(filename, 'r') as f:
	reader = csv.reader(f)
	header = next(reader)  # 読み込み

	for row in reader:
		print(row[1])       # intentsのファイル名、名前
		fname  = "./intents/" + row[1] + ".json"
		fname2 = "./intents/" + row[1] + "_usersays_ja.json"
		print(fname)

		# intentsファイル
		out_f = open(fname,'w')
		id = "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(4)])) + "-" +"".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(6)]))
		#out_f.write( id )
		out_f.write('{\n')
		str = "\t\"id\" : \"" + id + "\",\n"
		out_f.write(str)
		str = "\t\"name\" : \"" + row[1] + "\",\n"
		out_f.write(str)
		str = "\t\"auto\" : true,\n"
		out_f.write(str)
		str = "\t\"contexts\" : [],\n"
		out_f.write(str)
		str = "\t\"responses\" : [\n"
		out_f.write(str)
		str = "\t\t{"
		out_f.write(str)
		str = "\t\t\"resetContexts\": false,\n"
		out_f.write(str)
		str = "\t\t\"affectedContexts\": [],\n"
		out_f.write(str)
		str = "\t\t\"parameters\": [],\n"
		out_f.write(str)
		str = "\t\t\"messages\": [\n"
		out_f.write(str)
		str = "\t\t\t{\n"			# 通常メッセージの始まり
		out_f.write(str)
		str = "\t\t\t\"type\" : 0, \"lang\" : \"ja\", \"speech\" : \"" + row[2] + "\"\n"
		out_f.write(str)
		str = "\t\t\t},{\n"
		out_f.write(str)
		str = "\t\t\t\"type\" : 0, \"lang\" : \"ja\", \"speech\" : []\n"
		out_f.write(str)			# LINE用に追加するならこの行の次に入れる
		if len(row[6])>0:			# LINE用の文字列
			str = "\t\t\t},{\n"
			out_f.write(str)
			str = "\t\t\t\"type\" : 0, \"platform\" : \"line\", \"lang\" : \"ja\", \"speech\" : \"" + row[6] + "\"\n"
			out_f.write(str)
		if len(row[7])>0:			# LINE用の画像
			str = "\t\t\t},{\n"
			out_f.write(str)
			str = "\t\t\t\"type\" : 3, \"platform\" : \"line\", \"lang\" : \"ja\", \"imageUrl\" : \"" + row[7] + "\"\n"
			out_f.write(str)
		if len(row[8])>0:			# LINE用のボタン型選択肢
			str = "\t\t\t},{\n"
			out_f.write(str)
			str = "\t\t\t\"type\" : 2, \"platform\" : \"line\", \"lang\" : \"ja\", \"title\" : \"" + row[8] + "\", \"replies\" : ["
			out_f.write(str)
			if len(row[9])>0:			# LINE用のボタン型選択肢
				str = "\"" + row[9] + "\""
				out_f.write(str)
			if len(row[10])>0:			# LINE用のボタン型選択肢
				str = ",\"" + row[10] + "\""
				out_f.write(str)
			if len(row[11])>0:			# LINE用のボタン型選択肢
				str = ",\"" + row[11] + "\""
				out_f.write(str)
			str = "]\n"
			out_f.write(str)
		if len(row[12])>0:			# LINE用の画像付きボタン
			str = "\t\t\t},{\n"
			out_f.write(str)
			str = "\t\t\t\"type\" : 1, \"platform\" : \"line\", \"lang\" : \"ja\", \"title\" : \"" + row[12] + "\" , \"subtitle\" : \"" + row[13] + "\" , \"imageUrl\" : \"" + row[14] + "\" , \"buttons\" : ["
			out_f.write(str)
			if len(row[15])>0:			# LINE用のボタン型選択肢
				str = "{\"text\" : " + "\"" + row[15] + "\""
				out_f.write(str)
				if len(row[16])>0:			# LINE用のボタン型選択肢
					str = ",\"postback\" : " + "\"" + row[16] + "\""
					out_f.write(str)
				str = "}"
				out_f.write(str)
			if len(row[17])>0:				# LINE用のボタン型選択肢
				str = ",{\"text\" : " + "\"" + row[17] + "\""
				out_f.write(str)
				if len(row[18])>0:			# LINE用のボタン型選択肢
					str = ",\"postback\" : " + "\"" + row[18] + "\""
					out_f.write(str)
				str = "}"
				out_f.write(str)
			if len(row[19])>0:				# LINE用のボタン型選択肢
				str = ",{\"text\" : " + "\"" + row[19] + "\""
				out_f.write(str)
				if len(row[20])>0:			# LINE用のボタン型選択肢
					str = ",\"postback\" : " + "\"" + row[20] + "\""
					out_f.write(str)
				str = "}"
				out_f.write(str)

			str = "]\n"
			out_f.write(str)

		if len(row[21])>0:			# LINE用のCustom
			str = "\t\t\t},{\n"
			out_f.write(str)
			str = "\t\t\t\"type\" : 4, \"platform\" : \"line\", \"lang\" : \"ja\", \"payload\" : { \"line\" : " + row[21] + " }"
			out_f.write(str)

		# LINE用終わり
		str = "\t\t\t}\n\t\t],\n"
		out_f.write(str)
		str = "\t\t\"defaultResponsePlatforms\" : {},\n"
		out_f.write(str)
		str = "\t\t\"speech\" : []\n"
		out_f.write(str)
		str = "\t\t}\n\t],\n"
		out_f.write(str)
		str = "\t\"priority\": 500000, \"webhookUsed\" : false, \"webhookForSlotFilling\" : false, \"lastUpdate\" : 20190102, \"fallbackIntent\" : false, \"events\": []\n"
		out_f.write(str)
		str = "}\n"
		out_f.write(str)
		out_f.close

		#intentsのTraining pharaases
		out_f = open(fname2,'w')
		id = "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(4)])) + "-" +"".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(6)]))
		out_f.write('[\n\t{\n')
		str = "\t\t\"id\" : \"" + id + "\",\n"
		out_f.write(str)
		str = "\t\t\"data\" : [\n\t\t\t{\n"
		out_f.write(str)
		str = "\t\t\t\"text\" : \"" + row[1] + "\",\n"
		out_f.write(str)
		str = "\t\t\t\"userDefined\" : false\n"
		out_f.write(str)
		str = "\t\t\t}\n\t\t],\n"
		out_f.write(str)
		str = "\t\t\"isTemplate\": false, \"count\" : 0, \"updated\" : 20190102\n"
		out_f.write(str)
		str = "\t}"
		out_f.write(str)
		if len(row[3])>0:		#別の言い方
			id = "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(4)])) + "-" +"".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(6)]))
			out_f.write('\n\t,{\n')
			str = "\t\t\"id\" : \"" + id + "\",\n"
			out_f.write(str)
			str = "\t\t\"data\" : [\n\t\t\t{\n"
			out_f.write(str)
			str = "\t\t\t\"text\" : \"" + row[3] + "\",\n"
			out_f.write(str)
			str = "\t\t\t\"userDefined\" : false\n"
			out_f.write(str)
			str = "\t\t\t}\n\t\t],\n"
			out_f.write(str)
			str = "\t\t\"isTemplate\": false, \"count\" : 0, \"updated\" : 20190102\n"
			out_f.write(str)
			str = "\t}\n"
			out_f.write(str)
		if len(row[4])>0:		#別の言い方
			id = "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(4)])) + "-" +"".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(6)]))
			out_f.write('\n\t,{\n')
			str = "\t\t\"id\" : \"" + id + "\",\n"
			out_f.write(str)
			str = "\t\t\"data\" : [\n\t\t\t{\n"
			out_f.write(str)
			str = "\t\t\t\"text\" : \"" + row[4] + "\",\n"
			out_f.write(str)
			str = "\t\t\t\"userDefined\" : false\n"
			out_f.write(str)
			str = "\t\t\t}\n\t\t],\n"
			out_f.write(str)
			str = "\t\t\"isTemplate\": false, \"count\" : 0, \"updated\" : 20190102\n"
			out_f.write(str)
			str = "\t}\n"
			out_f.write(str)
		if len(row[5])>0:		#別の言い方
			id = "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(4)])) + "-" +"".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(2)])) + "-" + "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(6)]))
			out_f.write('\n\t,{\n')
			str = "\t\t\"id\" : \"" + id + "\",\n"
			out_f.write(str)
			str = "\t\t\"data\" : [\n\t\t\t{\n"
			out_f.write(str)
			str = "\t\t\t\"text\" : \"" + row[5] + "\",\n"
			out_f.write(str)
			str = "\t\t\t\"userDefined\" : false\n"
			out_f.write(str)
			str = "\t\t\t}\n\t\t],\n"
			out_f.write(str)
			str = "\t\t\"isTemplate\": false, \"count\" : 0, \"updated\" : 20190102\n"
			out_f.write(str)
			str = "\t}\n"
			out_f.write(str)		
		str = "\n]\n"
		out_f.write(str)
		out_f.close

#print "".join(map(lambda t: format(t, "02X"), [random.randrange(256) for x in range(16)]))


