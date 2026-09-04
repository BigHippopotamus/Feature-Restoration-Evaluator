import pandas as pd

from fre.misc import display_or_print

WARNING_NO_JIWER = """Could not import jiwer library. You will not be able to \
show word error rate info."""

try:
    import jiwer
except ModuleNotFoundError:
    print(WARNING_NO_JIWER)


# ====================
def wer_info(ref: str, hyp: str) -> dict:
    """Calculate reference length, minimum number of edits, and word
    error rate for a single reference+hypothesis pair."""

    len_ref = len(ref.split())
    num_edits = get_num_edits(ref, hyp)
    wer_ = wer(num_edits, len_ref)
    return {
        'len_ref': len_ref,
        'num_edits': num_edits,
        'wer': wer_
    }


# ====================
def get_num_edits(ref: str, hyp: str) -> int:
    """Get the minimum number of word edits required to get from
    hypothesis to reference string."""
    output = jiwer.process_words(ref, hyp)
    return output.substitutions + output.deletions + output.insertions


# ====================
def wer(num_edits: int, len_ref: int) -> float:
    """Calculate WER for minimum number of edits and reference length"""

    return num_edits / len_ref * 100


# ====================
def show_wer_info_table(wer_info: dict):
    """Show WER info in a table"""

    row_labels = [
        'Length of reference (words)',
        'Minimum edit distance (S+D+I)',
        'Word error rate (%)'
    ]
    wer_info_ = [
        f"{wer_info['len_ref']:,}",
        f"{wer_info['num_edits']:,}",
        f"{wer_info['wer']:.2f}%"
    ]
    display_or_print(pd.DataFrame(
        wer_info_, index=row_labels, columns=['Value']))
