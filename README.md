# screaming_channel_beta

## title 1
if I test this:

    bash cmd_collect.sh

Does it work?

# Run
First it is required to configure the receiver to correctly extract the individual traces.
This call will tune the SDR to 125.5MHz and will guide you through the following steps.
The file config/test.json will be created and all necessary parameter are stored in this file.

    python2 capture.py --config=config/test.json --dut=dut-openssl.py

In this case all 10 executions are clearly visible.

![alt tag](https://github.com/JeremyGUILLAUME/screaming_channel_beta/blob/main/IMGs/30meters.png)

To detect individual executions, a carrier that could act as a triggersignal is required.
