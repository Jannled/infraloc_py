-- ReactiveScript for PlotJuggler
-- Debug the arrays by printing them to the console

aoas = TimeseriesView.find("/aoa/angle")
freqs = TimeseriesView.find("/aoa/freq")

print("---- Begin ")
i = aoas:size()
while i>0 do
    print(aoas:at(i))
    i = i-1
end
print("----------------- a TOP")

i = freqs:size()
while i>0 do
    print(freqs:at(i))
    i = i-1
end
print("----------------- f TOP")