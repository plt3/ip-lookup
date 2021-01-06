function changeText() {
  const showText = "Click to show";
  const collapseText = "Click to collapse";
  if (event.target.innerHTML === showText) {
    event.target.innerHTML = collapseText;
  } else {
    event.target.innerHTML = showText;
  }
}
