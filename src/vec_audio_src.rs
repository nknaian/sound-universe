use std::time::Duration;
use rodio::Source;
use rand::{thread_rng, Rng};

pub struct VecAudioSrc {
    pub samples: Vec<u16>,
    sample_rate: u32,
    total_samples: usize,
    sample_num: usize,
}

impl VecAudioSrc {
    pub fn new(samples: Vec<u16>, sample_rate: u32, total_samples: usize) -> VecAudioSrc {
        VecAudioSrc {
            samples: samples as Vec<u16>,
            sample_rate: sample_rate as u32,
            total_samples: total_samples as usize,
            sample_num: 0
        }
    }

    pub fn add_noise(&mut self) {
        let mut rng = thread_rng();
        let sample_start: usize = rng.gen_range(0..(self.total_samples - 100));

        for sample in &mut self.samples[sample_start..sample_start+100] {
            *sample = rand::random::<u16>();
        }
    }
}

impl Iterator for VecAudioSrc {
    type Item = u16;

    fn next(&mut self) -> Option<u16> {
        self.sample_num = (self.sample_num + 1) % self.total_samples;
        let x = self.sample_num;
        match x {
            x if x <= self.total_samples => Some(self.samples[x]),
            _ => None,
        }   
    }
}

impl Source for VecAudioSrc {
    fn current_frame_len(&self) -> Option<usize> {
        None
    }

    fn channels(&self) -> u16 {
        1
    }

    fn sample_rate(&self) -> u32 {
        self.sample_rate
    }

    fn total_duration(&self) -> Option<Duration> {
        None
    }
}