#!/bin/bash -e

# check CLI parameters
if [ $# -lt 1 ]; then
	echo "need to specify some TAP files"
	exit 1
fi

# find the tape device using lsscsi -- assumes an Archive Python
TAPEDEV=$(lsscsi -g |grep ARCHIVE | sed -e 's_.*\(/dev/st[0-9]\+\).*_\1_' | sed 's_st_nst_')
TAPEGEN=$(lsscsi -g |grep ARCHIVE | sed -e 's_.*\(/dev/sg[0-9]\+\).*_\1_')

echo "Tape device is ${TAPEDEV}, generic device is ${TAPEGEN}"

# Leadin time in seconds
LEADIN=5

# Gap time in seconds
GAP=5

# Added silence to WAV files
WAVSILENCE=0
#WAVSILENCE=10

# WDAT command line -- force 44100 Hz
WDAT="$HOME/APPS/DAT/wdat_0.02/wdat -d ${TAPEGEN} -w -l ${LEADIN} -g ${GAP} -r 44100"


# if silence needs adding to WAV files, do so (sometimes the first block gets corrupted)
if [ $WAVSILENCE -gt 0 ]; then
	sox -n -r 44100 -b 16 -c 2 silence.wav trim 0.0 ${WAVSILENCE}.0
fi


echo "converting Jupiter Ace TAP files to WAV..."


L=""
for i in $@; do
	echo "... ${i}"

	# convert TAP to WAV
	ONM=$(basename $i .tap)
	castool convert jupiter $i $ONM.wav

	# WDAT needs Stereo 44100 uncompressed WAV files
	sox $ONM.wav -c 2 ${ONM}_pre.wav

	# Prepend WAV silence if required
	if [ $WAVSILENCE -gt 0 ]; then
		sox silence.wav ${ONM}_pre.wav ${ONM}_st.wav
	else
		mv ${ONM}_pre.wav ${ONM}_st.wav
	fi

	# add to list
	L="$L ${ONM}_st.wav"

	# delete original wav files
	rm -f $ONM.wav ${ONM}_pre.wav
done

echo "writing DAT tape..."

mt -f ${TAPEDEV} status
mt -f ${TAPEDEV} rewind
#echo
#mt -f ${TAPEDEV} status
#echo

# write to DAT
$WDAT $L

# tidy up
rm -f $L silence.wav

mt -f ${TAPEDEV} rewind
mt -f ${TAPEDEV} eject

