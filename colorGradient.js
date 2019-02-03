var perc = ((avgSpeed - minSpeed)/(maxSpeed - minSpeed);

function colorGradient(perc) {
 var r, g, b = 0;
  if (perc < 50) {
    r = 255;
    g = Math.round(5.1 * perc);
  }
  else {
    g = 255;
    r = Math.round(510 - 5.10 * perc);
  }
  var h = g * 0x10000 + r * 0x100 + b * 0x1;
  return '#' + ('000000' + h.toString(16)).slice(-6);
}
