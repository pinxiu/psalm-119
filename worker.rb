STDOUT.sync = true
puts "Starting up"

trap('TERM') do
  exec('./push')
  puts "Backing up"
  exit
end

