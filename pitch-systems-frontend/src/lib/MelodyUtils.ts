import Melody from "./Melody";
import type PSClient from "./PSClient";
import type { Interval, Cents } from "./APITypes";


/**
 * Get the cents values and analysis of the melody object from the list of frequencies assigned to it.
 * 
 * @param melody 
 * @param psclient 
 * @returns Promise<Melody>
 */
export const getAnalysis = async (melody: Melody, psclient: PSClient): Promise<Melody> => {
    const cents = await psclient.getCents(melody.getUniqueFrequencies(), melody.root);

    //Check intervals matching each cents value and its octave equivalent
    const check_cents = cents.map((c) => c.cents).concat(cents.map((c) => c.cents % 1200));
    const intervals = await psclient.getIntervals(check_cents);

    melody.cents = cents;
    //Assign intervals to cents values
    for (const cents of melody.cents) {
        const match = intervals.find((i) => i.cents == cents.cents);
        if (match) {
            console.log(`Matched ${cents.cents} to ${match.cents}`)
            melody.intervals[cents.cents] = match;
        } else {
            const octave_match = intervals.find((i) => i.cents == cents.cents % 1200);
            console.log(intervals)
            if (octave_match) {
                console.log(`No match. Octave match ${cents.cents} to ${octave_match.cents}`)
                melody.intervals[cents.cents] = octave_match;
            } else {
                console.log(`No octave match for ${cents.cents}`)
            }
        }
   }

   //No point querying all scales if only the unison interval is being checked.
   const int_matches = melody.getSelectedIntervals();
   if (int_matches.length > 1 || int_matches[0].cents != 0) {
        const scales = await psclient.getScales(int_matches);
        melody.scales = scales;
   }

    return melody;
}

/**
 * Update the melody root frequency, and refresh the analysis.
 * 
 * @param root 
 * @returns Promise<Melody>
 */
export const updateRoot = async(root: number, melody: Melody, psclient: PSClient): Promise<Melody> => {
    melody.root = root;
    return await getAnalysis(melody, psclient);
}

/**
 * Update the melody with a new interval selection and refresh the matching scales.
 * @param cents 
 * @param interval 
 * @param melody 
 * @param psclient 
 * @returns Promise<Melody>
 */
export const updateInterval = async (cents: number, interval: Interval, melody: Melody, psclient: PSClient): Promise<Melody> => {
    melody.setInterval(cents, interval);
    const scales = await psclient.getScales(melody.getSelectedIntervals());
    melody.scales = scales;
    return melody;
};

/**
 * Remove a cents value from the melody and any interval matching it.
 * 
 * @param item
 * @param melody
 * @returns Melody
 */
export const removeCents = async (item: Cents, melody: Melody, psclient: PSClient): Promise<Melody> => {
    melody.cents = melody.cents.filter((c) => c !== item);
    delete melody.intervals[item.cents];

    const scales = await psclient.getScales(melody.getSelectedIntervals());
    melody.scales = scales;
    return melody;
};