import dayjs from 'dayjs'

export const convertDate = (date, formetString) => {
  formetString = formetString || 'YYYY-MM-DDTHH:mm:s'
  date = date || new Date()

  if (dayjs(date).isValid()) {
    if (dayjs(date).year() >= 9999) {
      return dayjs(date).year(9999).format(formetString)
    } else {
      return dayjs(date).format(formetString)
    }
  } else {
    return ''
  }
}
