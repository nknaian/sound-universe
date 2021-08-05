use std::fs::File;
use std::io::BufReader;
use std::time::Duration;

//use rand;

use rodio::{Decoder, OutputStream, Sink};
use rodio::source::{Source};

mod vec_audio_src;

// 44100 Hz sample rate
const SAMPLE_RATE: u32 = 44100;

// Length of loop
// const LOOP_LENGTH_SEC: u64 = 2;

// Two second loop at 44100 Hz
// const TOTAL_SAMPLES: usize = (LOOP_LENGTH_SEC as usize) * (SAMPLE_RATE as usize);

fn main() {
    // Get default sink
    let (_stream, stream_handle) = OutputStream::try_default().unwrap();
    let sink = Sink::try_new(&stream_handle).unwrap();
    
    // Create empty samples vector
    // let mut samples: Vec<u16> = Vec::new();

    // Fill vector with random values
    // for _sample in 0..TOTAL_SAMPLES {
    //     samples.push(rand::random::<u16>())
    // }

    // Fill vector with values from sound
    let file = BufReader::new(File::open("mixkit-arcade-retro-background-219.wav").unwrap());
    let file_source = Decoder::new(file).unwrap();
    let samples: Vec<u16> = file_source.convert_samples().collect();
    let total_samples = samples.len();
    println!("Number of samples = {}", total_samples);

    // Create source from samples
    let source = vec_audio_src::VecAudioSrc::new(samples, SAMPLE_RATE, total_samples);

    // Setup periodic access every 10 ms to the source
    let periodic_access_source = source.periodic_access(Duration::from_millis(10), &access);

    // Append source onto sink for playback
    sink.append(periodic_access_source);
    
    // The sound plays in a separate thread. This call will block the current thread until the sink
    // has finished playing all its queued sounds.
    sink.sleep_until_end();
}

pub fn access(vec_audio_src: &mut vec_audio_src::VecAudioSrc) {
    vec_audio_src.add_noise();
}


// mod audio_buf {
//     use std::time::Duration;
//     use rodio::Source;
//     use rand::{thread_rng, Rng};

//     pub struct VecAudioSrc {
//         pub samples: Vec<u16>,
//         sample_rate: u32,
//         total_samples: usize,
//         sample_num: usize,
//     }

//     impl VecAudioSrc {
//         pub fn new(samples: Vec<u16>, sample_rate: u32, total_samples: usize) -> VecAudioSrc {
//             VecAudioSrc {
//                 samples: samples as Vec<u16>,
//                 sample_rate: sample_rate as u32,
//                 total_samples: total_samples as usize,
//                 sample_num: 0
//             }
//         }

//         pub fn add_noise(&mut self) {
//             let mut rng = thread_rng();
//             let sample_start: usize = rng.gen_range(0..(self.total_samples - 100));

//             for sample in &mut self.samples[sample_start..sample_start+100] {
//                 *sample = rand::random::<u16>();
//             }
//         }
//     }

//     impl Iterator for VecAudioSrc {
//         type Item = u16;

//         fn next(&mut self) -> Option<u16> {
//             self.sample_num = (self.sample_num + 1) % self.total_samples;
//             let x = self.sample_num;
//             match x {
//                 x if x <= self.total_samples => Some(self.samples[x]),
//                 _ => None,
//             }   
//         }
//     }

//     impl Source for VecAudioSrc {
//         fn current_frame_len(&self) -> Option<usize> {
//             None
//         }

//         fn channels(&self) -> u16 {
//             1
//         }

//         fn sample_rate(&self) -> u32 {
//             self.sample_rate
//         }

//         fn total_duration(&self) -> Option<Duration> {
//             None
//         }
//     }
// }