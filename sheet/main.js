//Modified Emad Adel
//https://github.com/emadadeldev/

function skipMatch(match) {
  switch (match) {
    case "~rp~":
    case "~n~":
    case "~m~":
      return true;
    default:
      return false;
  }
}


function FixedLineCode(text_en, text_ar) {

  const regex = /~(.*?)~/g;
  if (text_en == null || text_ar == null) {
    return [];
  }



  let match;
  /*
  while ((match = regex.exec(text_ar)) !== null) {
      if (skipMatch(match[0])) {
          continue;
      }
      if (!text_en.includes(match[0])) {
          appendLine("errorsar.txt", `Error: ${text_hash} ${match[0]}`);
      }
  }
  */
  // Reset the regex index to re-use the regex on another string
  regex.lastIndex = 0;


  // Loop through English text matches
  while ((match = regex.exec(text_en)) !== null) {
    if (skipMatch(match[0])) {
      continue;
    }

    if (!text_ar.includes(match[0])) {
      return true;
    }
  }

  return false;
}


function FixedLineCodes(text_en, text_ar) {

  const regex = /~(.*?)~/g;
  if (text_en == null || text_ar == null) {
    return [];
  }


text_en=text_en+"";
text_ar=text_ar+"";


  let match;
  var arcount = 0;
  while ((match = regex.exec(text_ar)) !== null) {
    if (skipMatch(match[0])) {
      continue;
    }
      arcount++;
  }

  // Reset the regex index to re-use the regex on another string
  regex.lastIndex = 0;

  var encount = 0;
  // Loop through English text matches
  while ((match = regex.exec(text_en)) !== null) {

    if (skipMatch(match[0])) 
    {
      continue;
    }
      encount++;
  }

  regex.lastIndex = 0;



  if (arcount === encount) {
      text_ar = text_ar.replace(/~(.*?)~/g, function (item) {
        while ((match = regex.exec(text_en)) !== null) {
          //console.log(match);
          return match[0];
        }

        return item;

      });
  

  }



  return text_ar;
}



console.log(
  FixedLineCodes("~sl:0.0:5.8~Purity. That is what they are paying the big price for,~sl:~and that is what Marcel has created, is it not?", "~sl:0.0:5.8~النقاء. هذا هو ما يدفعون الثمن الباهظ من أجله، ~sl:0.0:5.8~وهذا ما صنعه (مارسيل)، أليس كذلك؟")
);




function FixedLines(input) {
  const lines = [];
  for (let i = 0; i < input.length; i++) {
    ;
    lines.push(FixedLineCode(input[i][0], input[i][1]));
  }

  return lines;
}


function FixedLines1(input) {
  const lines = [];
  for (let i = 0; i < input.length; i++) {
    ;
    lines.push(FixedLineCodes(input[i][0], input[i][1]));
  }

  return lines;
}

//console.log(FixColors("أمتطي خيلك و أتبع~o~(هوزيا)~s~"));
console.log(ConvertToEngineText(("يبدو أن السيرك في البلدة.~n~~m~اذهبوا للمنزل!")));

function swapColors(text) {
  const reversedCodes = text.match(/~[oedi]~.*?~s~/g);
  if (reversedCodes) {
    reversedCodes.forEach((code) => {
      const reversed = code.replace(/~([oedi])~(.*?)~s~/, "~s~$2~$1~");
      text = text.replace(code, reversed);
    });
  }

  return text;
}


function ConvertTable(input) {
  const lines = [];

  for (let i = 0; i < input.length; i++) {
    const line = input[i][0];
    lines.push(line);
  }

  return lines;
}


function ConvertToEngineText(input, SplitLine = false, SplitNum = 0, BreakLine = "") {

  if (typeof SplitNum !== 'number' || SplitNum === 0) {
    SplitLine = false;
  }

  return Array.isArray(input) ?
    input.map(row => row.map(cell => ConvertText(cell, SplitLine, SplitNum, BreakLine))) :
    ConvertText(input, SplitLine, SplitNum, BreakLine);
}


function Textsplit(text, regex) {
  var token, index, result = [];
  while (text !== '') {
    regex.lastIndex = 0;
    token = regex.exec(text);
    if (token === null) {
      break;
    }
    index = token.index;
    if (token[0].length === 0) {
      index = 1;
    }
    result.push(text.substr(0, index));
    result.push(token[0]);
    index = index + token[0].length;
    text = text.slice(index);
  }
  result.push(text);
  return result;
}



function ConvertText(Text, SplitLine = false, SplitNum = 0, BreakLine = "") {

  var arabicRegex = /[ٮ-ۯ؀-ٟﭐ-ﻼ]+/gm;

  if (!arabicRegex.test(Text)) {
    return Text;
  }

  var ll = swapColors(Text + "").replace(/~rp~/gm, " ");


  //|\~s\~|\~o\~|\~e\~|\~d\~|\~i\~
  Lines = Textsplit(ll, /\~lr:.*?\~|\~sl:.*?\~|\~n\~/gm);
  for (i = 0; i < Lines.length; i++) {

    const reversedCodes = Lines[i].match(/^(~.*?~)(.*)/g);
    if (reversedCodes) {
      reversedCodes.forEach((code) => {
        const reversed = code.replace(/^(~.*?~)(.*)/, "$2$1");
        Lines[i] = Lines[i].replace(code, reversed);
      });
    }


    Lines[i] = ConvertText1(Lines[i], SplitLine, SplitNum, BreakLine)
  }

  return Lines.join('').trim("\n").trim("\r");
}



function ConvertText1(text, SplitLine = false, SplitNum = 0, BreakLine = "") {

  Codes = [];
  var text = text + "";
  if (text == "") { return; }
  if (!text.match(/[ٮ-ۯ؀-ٟﭐ-ﻼ]/gm)) { return text; }

  if (SplitLine) {

    text = SplitText(text, BreakLine, SplitNum)

    text = convertArabic(text + "");


  } else {
    text = convertArabic(text + "");
  }




  SplitString = text.split(/\r?\n/);
  for (f = 0; f < SplitString.length; f++) {

    SplitString[f] = wordsReverser(SplitString[f]);
  }

  text = SplitString.join("\n");

  return text;
}




function SplitText(input, breakc, len) {
  SplitStringInput = "";
  breaklinecodeInput = "";
  SplitNumInput = "";
  var SplitStringInput = input + "";
  var breaklinecodeInput = breakc + "";

  var SplitNumInput = len;

  if (breaklinecodeInput == "$newline") {
    breaklinecodeInput = "\r\n";
  }
  var SplitString = [{}];

  SplitString = SplitStringInput.split(/\r?\n/);
  for (f = 0; f < SplitString.length; f++) {
    finaltext = "";
    text = SplitString[f];
    var idealSplit = SplitNumInput,
      lineCounter = 0,
      lineIndex = 0,
      theString = "",
      lines = [""],
      ch,
      i;

    for (i = 0; i < text.length; i++) {
      ch = text[i];
      if (ch == "[") {
        var startIndex = i;
        var endIndex = text.indexOf("]", i + 1);

        if (endIndex !== -1) {
          var section = text.substring(startIndex, endIndex + 1);
          lines[lineIndex] += section;
          i = endIndex;
          // lineCounter += section.length;
          continue;
        }
      }

      if (ch == "~") {
        var startIndex = i;
        var endIndex = text.indexOf("~", i + 1);

        if (endIndex !== -1) {
          var section = text.substring(startIndex, endIndex + 1);
          lines[lineIndex] += section;
          i = endIndex;
          // lineCounter += section.length;
          continue;
        }
      }

      if (lineCounter >= idealSplit && ch === " ") {
        ch = "";
        lineCounter = -1;
        lineIndex++;
        lines.push("");
      }
      lines[lineIndex] += ch;
      lineCounter++;
    }
    setbreakline = false;
    for (e = 0; e < lines.length; e++) {
      if (setbreakline == false) {
        finaltext = lines[e] + finaltext;
        setbreakline = true;
      } else {
        if (breaklinecodeInput == "\r\n") {
          finaltext = finaltext + breaklinecodeInput + lines[e];
        } else {
          finaltext = lines[e] + breaklinecodeInput + finaltext;
        }
      }
    }
    SplitString[f] = finaltext;
  }
  var theString = SplitString.join("\r\n");
  return theString;
}