import uhd
import numpy as np


def usrp_init(usrp, center_freq, sampling_rate, gain=40):
	usrp.set_rx_rate(sampling_rate, 0)
	usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(center_freq), 0)
	usrp.set_rx_gain(gain, 0)
	usrp.set_rx_antenna("TX/RX") #TX/RX, RX2

	# Set up the stream and receive buffer
	st_args = uhd.usrp.StreamArgs("fc32", "sc16")
	st_args.channels = [0]
	streamer = usrp.get_rx_stream(st_args)
	return streamer


def usrp_start(streamer):
	stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
	stream_cmd.stream_now = True
	streamer.issue_stream_cmd(stream_cmd)


def usrp_stop(streamer):
	stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
	streamer.issue_stream_cmd(stream_cmd)
	

def usrp_get_data(streamer, num_samps, drop_start):
	recv_buffer = np.zeros((1, num_samps), dtype=np.complex64)
	metadata = uhd.types.RXMetadata()
	nb_samples = streamer.recv(recv_buffer, metadata)
	samples = recv_buffer[0]
	samples = np.absolute(samples)
	#samples = np.real(samples)
	#samples = np.imag(samples)
	samples = samples[drop_start:]

	recv_buffer_ = np.zeros((1, num_samps), dtype=np.complex64)
	while nb_samples != 0:
		nb_samples = streamer.recv(recv_buffer_, metadata)

	return samples
