import matplotlib.pyplot as plt
import numpy as np

PATH = "./ping_output.txt"
ORIGINAL_HOST = "developer.mozilla.org"
ACTUAL_IP = "34.111.97.67"

def parse_ping_line(line):
    """ Recieves a ping line and retuern the time in ms and the timestamp
    Example: [1728173874.915759] 64 bytes from 67.97.111.34.bc.googleusercontent.com (34.111.97.67): icmp_seq=7200 ttl=117 time=24.2 ms"""
    time = line.split("time=")[1].split(" ")[0]
    timestamp = line.split("[")[1].split("]")[0]
    icmp_seq = line.split("icmp_seq=")[1].split(" ")[0]
    return {
        "time": time,
        "timestamp": timestamp,
        "icmp_seq": icmp_seq
    }

def parse_total_line(line):
    """ Recieves a total line and returns the packet transmitted, packet received, packet loss and total time
    Example: 7200 packets transmitted, 7200 received, 0% packet loss, time 7212733ms"""
    packet_transmitted = int(line.split(" ")[0])
    packet_received = int(line.split(" ")[3])
    packet_loss = float(line.split(" ")[5].split("%")[0])
    total_time = float(line.split(" ")[9].split("ms")[0])

    return packet_transmitted, packet_received, packet_loss, total_time

def parse_rtt_line(line):
    """ Recieves a rtt line and returns the min, avg, max and mdev
    Example: rtt min/avg/max/mdev = 10.645/28.369/660.327/26.176 ms"""
    rtt_min = float(line.split(" ")[3].split("/")[0])
    rtt_avg = float(line.split(" ")[3].split("/")[1])
    rtt_max = float(line.split(" ")[3].split("/")[2])
    rtt_mdev = float(line.split(" ")[3].split("/")[3])

    return rtt_min, rtt_avg, rtt_max, rtt_mdev

def is_ping_line(line):
    """ Returns True if the line is a ping line, False otherwise"""
    return "time=" in line

def is_total_line(line):
    """ Recieves a total line and returns the packet transmitted, packet received, packet loss and total time"""
    return "packets transmitted" in line

def is_rtt_line(line):
    """ Returns True if the line is a rtt line, False otherwise"""
    return "rtt" in line

def main():

    pings = []

    packet_transmitted = 0
    packet_received = 0
    packet_loss = 0
    total_time = 0

    rtt_min = 0
    rtt_avg = 0
    rtt_max = 0
    rtt_mdev = 0    

    with open(PATH, "r") as file:
        for line in file:
            if is_ping_line(line):
                pings.append(parse_ping_line(line))
            elif is_total_line(line):
                packet_transmitted, packet_received, packet_loss, total_time = parse_total_line(line)
            elif is_rtt_line(line):
                rtt_min, rtt_avg, rtt_max, rtt_mdev = parse_rtt_line(line)

    print("Packet transmitted: ", packet_transmitted)
    print("Packet received: ", packet_received)
    print("Packet loss: ", packet_loss)
    print("Total time: ", total_time)
    print("")
    print("RTT Min: ", rtt_min)
    print("RTT Avg: ", rtt_avg)
    print("RTT Max: ", rtt_max)
    print("RTT Mdev: ", rtt_mdev)
    print("")
    
    # i want the average of every 100 pings
    
    seqs = [int(ping["icmp_seq"]) for ping in pings]
    times = [float(ping["time"]) for ping in pings]

    step = 100

    seqs_avg = []
    times_avg = []

    for i in range(0, len(seqs), step):
        seqs_avg.append(seqs[i] - seqs[0])
        times_avg.append(np.mean([float(times[j]) for j in range(i, i+step)]))
        
    
    plt.figure(figsize=(10, 6))
    plt.plot(seqs_avg, times_avg, label="Ping Time")
    plt.xlabel("Ping Number")
    plt.ylabel("Ping Time (ms)")
    plt.title(f"Ping Time to {ORIGINAL_HOST} ({ACTUAL_IP})")
    plt.savefig("rtt_vs_tiempo.png")
    print("Plot saved as rtt_vs_tiempo.png")

    # now i want to group the pings by time so i can see the distribution of the pings

    bins = 25

    plt.figure(figsize=(10, 6))
    plt.hist(times, bins=bins)
    plt.xlabel("Ping Time (ms)")
    plt.ylabel("Frequency")
    plt.title(f"Ping Time to {ORIGINAL_HOST} ({ACTUAL_IP})")
    plt.savefig("rtt_distribution.png")
    print("Plot saved as rtt_distribution.png")

    # now the same but with a log log scale

    plt.figure(figsize=(10, 6))
    plt.hist(times, bins=bins)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel("Ping Time (ms)")
    plt.ylabel("Frequency")
    plt.title(f"Ping Time to {ORIGINAL_HOST} ({ACTUAL_IP})")
    plt.savefig("rtt_distribution_log.png")
    print("Plot saved as rtt_distribution_log.png")

    

if __name__ == "__main__":
    main()