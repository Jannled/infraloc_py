-- ReactiveScript for PlotJuggler
-- Three different data are published under the same topic, 
-- split them into different topics

-- NOTE: Copy these lines into the `Global code, execute once:` textarea
angle_1 = Timeseries.new("angle/1")
angle_2 = Timeseries.new("angle/2")
angle_3 = Timeseries.new("angle/3")

rssi_1 = Timeseries.new("rssi/1")
rssi_2 = Timeseries.new("rssi/2")
rssi_3 = Timeseries.new("rssi/3")

last_tick = 0

freq_1 = 12500
freq_2 = 15625
freq_3 = 18750

-- NOTE: Copy these lines intro the `Function Library` pane
-- Safely compare Floating point numbers
function fequals(a, b)
    return math.abs(a - b) < 0.0000001
end

-- NOTE: Copy the *contents* of this function into `function(tracker_time)` textarea
function call(tracker_time)
    aoas = TimeseriesView.find("/aoa/angle")
    freqs = TimeseriesView.find("/aoa/freq")
    rssis = TimeseriesView.find("/aoa/rssi")

    -- Filter out nil
    if aoas == nil or freqs == nil then
        print("[ERR] nil in data")
        return
    end

    -- Make sure no time overflow happened
    if last_tick > tracker_time then
        print("Scrubbing in the past")
        return
    end

    -- Sanity check array length
    if aoas:size() ~= freqs:size() then
        print("[ERR] data series don't have the same length")
        return
    end

    i = freqs:size()
    while i > 0 do
        t_freq, current_freq = freqs:at(i)
        t_ang, current_angle = aoas:at(i)
        t_rssi, current_rssi = rssis:at(i)
        
        -- End the loop when the timestamp of the last call is found
        if fequals(t_freq, last_tick) then break end
        
        -- Filter out nil
        if current_freq == nil or current_angle == nil then
            print("[ERR] datapoint is nil")
            return
        end
        
        -- Angle and Freq at the same index should also have the same time
        if not fequals(t_freq, t_ang) then
            print("[ERR] (" .. i .. ") " .. t_freq .. "!=" .. t_ang)
            -- return
        end

        -- Sort by frequency
        if fequals(current_freq, freq_1) then
            angle_1:push_back(t_ang, current_angle)
            rssi_1:push_back(t_rssi, current_rssi)
        elseif fequals(current_freq, freq_2) then
            angle_2:push_back(t_ang, current_angle)
            rssi_2:push_back(t_rssi, current_rssi)
        elseif fequals(current_freq, freq_3) then
            angle_3:push_back(t_ang, current_angle)
            rssi_3:push_back(t_rssi, current_rssi)
        end
        i = i-1
    end

    last_tick = tracker_time
end
