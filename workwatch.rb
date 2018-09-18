require 'date'
require 'json'

today = Date.today

def format_time(timestamp)
  Time.at(timestamp).strftime("%H:%M")
end

4.downto 0 do |n|
  date = today - n
  log = `journalctl --since #{date} --until #{date + 1} -o json`.lines.map do |line|
    JSON.parse(line)["__REALTIME_TIMESTAMP"].to_i / (1000 * 1000)
  end

  if log.length == 0
    next
  end

  puts date
  last = log[0]
  start = log[0]
  log.drop(1).each do |record|
    if last + 60 * 10 < record
      puts "#{format_time(start)} - #{format_time(last)}"
      start = record
    end
    last = record
  end
  puts "#{format_time(start)} - #{format_time(last)}"
  puts
end