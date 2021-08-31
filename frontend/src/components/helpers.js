import { timeFormat } from "d3-time-format";


export function fromToDates(date) {
  if(date == undefined) return
  var strDate = `${date.substr(0,4)}-${date.substr(4,2)}-${date.substr(6,2)}T00:00:00.000-05:00`
  var date = new Date(strDate)
  var start = new Date(strDate)
  var end = new Date(strDate)
  var dayMS = 86400000 //24*60*60*1000 milisenconds in a day
  if (date.getDay() === 1) dayMS = dayMS * 3; //3 days
  start.setTime(date.getTime() - dayMS);
  var dayMS = 86400000
  if (date.getDay() === 5) dayMS = dayMS * 3; // its friday so add 3 days
  end.setTime(date.getTime() + dayMS);
  var format = timeFormat('%Y%m%d')
  console.log('ftdates',format(start), format(end))
  return {from:format(start), to:format(end)}
}


export function fromGpedSlugToStartEndDates(slug) {
  //CEMI-trades-by-varveler-on-jul-22-2021-b1ab8977
  if(slug == undefined) return
  var l = slug.split('-')
  var month = l[5]
  var day = l[6]
  var year = l[7]
  var strDate = `${day} ${month} ${year} 00:00:00.000-05:00`
  var date = new Date(strDate)
  var start = new Date(strDate)
  var end = new Date(strDate)
  var dayMS = 86400000 //24*60*60*1000 milisenconds in a day
  if (date.getDay() === 1) dayMS = dayMS * 3; //3 days
  start.setTime(date.getTime() - dayMS);
  var dayMS = 86400000
  if (date.getDay() === 5) dayMS = dayMS * 3; // its friday so add 3 days
  end.setTime(date.getTime() + dayMS);
  var format = timeFormat('%Y%m%d')
  console.log('ftdates',format(start), format(end))
  return {from:format(start), to:format(end)}
}

export function dateTimeFromStrToFormatedStr(date) {
  var d = new Date(date)
  var format = timeFormat('%B %d, %Y at %H:%M')
  return format(d)
}
