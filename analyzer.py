def find_spikes(scarabs, min_chaos=2, spike_threshold=10):
    opportunities = []

    for scarab in scarabs:
        name = scarab['name']
        chaos_value = scarab['chaosValue']
        change = scarab.get("sparkline", {}).get("totalChange", 0)

        #Only care about scarabs worth atleast 2c and rising by 10% or more
        if chaos_value >= min_chaos and change >= spike_threshold:
            opportunities.append({
                "name": name,
                "chaos_value": chaos_value,
                "change": change
            })

    #sort big spikes first
    opportunities.sort(key=lambda x: x['change'], reverse=True)

    return opportunities
    