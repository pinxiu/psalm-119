trap('TERM') do
  exec('./push')
  exit
end

