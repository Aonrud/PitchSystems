import type Melody from "./Melody";
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
    const intervals = await psclient.getIntervals(cents.map((c) => c.cents));

    melody.setCents(cents);
    for (const interval of intervals) {
        melody.intervals[interval.cents] = interval;
    }

    const scales = await psclient.getScales(melody.getSelectedIntervals());
    melody.scales = scales;

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
export const removeCents = (item: Cents, melody: Melody): Melody => {
    melody.cents = melody.cents.filter((c) => c !== item);
    delete melody.intervals[item.cents];
    
    return melody;
};