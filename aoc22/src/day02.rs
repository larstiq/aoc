#![allow(dead_code)]

use std::convert::TryInto;

#[allow(unused_imports)]
use anyhow;

pub fn day02() {
    println!("day02 part1: {}", part1(&input()));
    println!("day02 part2: {}", part2(&input()));
}

#[derive(Debug, Clone, Copy)]
enum RPS {
    Rock = 0,
    Paper = 1,
    Scissors = 2,
}

impl RPS {
    fn fight(&self, other: &Self) -> i32 {
        let diff = (*self as i8) - (*other as i8);
        match diff.rem_euclid(3) {
            0 => 3,
            1 => 0,
            2 => 6,
            i8::MIN..=-1_i8 | 3_i8..=i8::MAX => todo!(),
        }
    }

    fn strategy(&self, strategy: u8) -> (Self, Self) {
        let other = match strategy as char {
            'X' => (*self as i32 + 2).rem_euclid(3).try_into(), // Other should lose against self
            'Y' => Ok(*self),                                   // Draw the matchup
            'Z' => (*self as i32 + 1).rem_euclid(3).try_into(),
            _ => todo!(), // Should not happen
        };
        (*self, other.unwrap())
    }
}

impl TryFrom<i32> for RPS {
    type Error = i32;

    fn try_from(v: i32) -> Result<RPS, i32> {
        match v {
            0 => Ok(RPS::Rock),
            1 => Ok(RPS::Paper),
            2 => Ok(RPS::Scissors),
            _ => Err(v),
        }
    }
}

impl TryFrom<char> for RPS {
    type Error = i32;

    fn try_from(v: char) -> Result<RPS, i32> {
        match v {
            'A' | 'B' | 'C' => ((v as i32) - ('A' as i32)).try_into(),
            'X' | 'Y' | 'Z' => ((v as i32) - ('X' as i32)).try_into(),
            _ => Err(-1),
        }
    }
}

fn score(matchups: Vec<(RPS, RPS)>) -> i32 {
    matchups
        .iter()
        .map(|(opp, you)| 1 + (*you as i32) + opp.fight(you))
        .sum()
}

fn part1(input: &str) -> i32 {
    let matchups: Vec<(RPS, RPS)> = input
        .lines()
        .map(|line| {
            let bytes = line.as_bytes();
            let (opp, you) = (bytes[0] as char, bytes[2] as char);
            (
                opp.try_into().expect("opponent part1"),
                you.try_into().expect("you part1"),
            )
        })
        .collect();
    score(matchups)
}

fn part2(input: &str) -> i32 {
    let matchups: Vec<(RPS, RPS)> = input
        .lines()
        .map(|line| {
            let bytes = line.as_bytes();
            let opp: RPS = (bytes[0] as char).try_into().unwrap();
            opp.strategy(bytes[2])
        })
        .collect();
    score(matchups)
}

fn input() -> String {
    std::fs::read_to_string("inputs/02").expect("inputs/02 to exist")
}

fn example() -> String {
    std::fs::read_to_string("examples/02").expect("examples/02 to exist")
}

#[test]
fn test_part1() {
    assert_eq!(15, part1(&example()));
    assert_eq!(12, part2(&example()));
}
